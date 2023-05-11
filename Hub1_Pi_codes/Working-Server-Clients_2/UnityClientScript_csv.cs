using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.IO;

public class UnityClientScript_csv : MonoBehaviour
{
    private class ReceivedData
    {
        public string HubPrefix; // Hub prefix for received data
        public byte[] Data; // Byte array of received data
        public int BytesRead; // Number of bytes read from the received data
    }

    private string serverIP; // IP address of the server to connect to
    private int port = 8000; // Port number of the server to connect to
    private string saveFolderPath; // Path of the folder to save the received data
    private string fileName = "sensor_data_"; // Name of the file to save the received data
    private int fileCounterHub1 = 0; // Counter for the number of files saved for Hub1
    private int fileCounterHub2 = 0; // Counter for the number of files saved for Hub2
    private Queue<ReceivedData> receivedDataQueue = new Queue<ReceivedData>(); // Queue to store received data

    private bool isRunning = true; // Flag to indicate whether the client is still running
    private Thread clientThread; // Thread for running the client

    void Start()
    {
        serverIP = GetLocalIPAddress(); // Get the local IP address of the client
        Thread clientThread = new Thread(new ThreadStart(ClientThread)); // Create a new thread for the client
        clientThread.Start(); // Start the client thread
    }

    void OnDestroy()
    {
        isRunning = false; // Set the isRunning flag to false to stop the client
        if (clientThread != null && clientThread.IsAlive)
        {
            clientThread.Join(); // Wait for the client thread to finish
        }
    }

    void Update()
    {
        while (receivedDataQueue.Count > 0) // Process received data in the queue
        {
            ReceivedData receivedData;
            lock (receivedDataQueue)
            {
                receivedData = receivedDataQueue.Dequeue(); // Dequeue the received data
            }
            // Get the hub prefix of the received data
            string hubPrefix = receivedData.HubPrefix; 
            // Determine the folder path based on the hub prefix
            string folderPath = hubPrefix == "Hub1" ? "Hub1_data" : "Hub2_data"; 
            // Combine the folder path with the application path
            saveFolderPath = Path.Combine(Application.dataPath, folderPath); 
            Directory.CreateDirectory(saveFolderPath); // Create the folder if it doesn't exist

            FileStream fileStream = null;
            // Combine the file path with the hub prefix and file counter
            string filePath = Path.Combine(saveFolderPath, hubPrefix + "_" + fileName + (hubPrefix == "Hub1" ? fileCounterHub1 : fileCounterHub2) + ".csv"); 
            Debug.Log("Saving data to file: " + filePath);
            fileStream = new FileStream(filePath, FileMode.CreateNew, FileAccess.Write); // Create a new file with the specified file path

            fileStream.Write(receivedData.Data, 0, receivedData.BytesRead); // Write the received data to the file

            if (hubPrefix == "Hub1")
            {
                fileCounterHub1++; // Increment the file counter for Hub1
            }
            else
            {
                fileCounterHub2++; // Increment the file counter for Hub2
            }

                    Debug.Log("File counter Hub1: " + fileCounterHub1 + ", File counter Hub2: " + fileCounterHub2);

        fileStream.Close(); // Close the file stream to release the file lock and allow other processes to access the file
    }
}

// This method runs on a separate thread to communicate with the server and receive data
void ClientThread()
{
    Debug.Log("Starting ClientThread");

    while (isRunning)
    {
        try
        {
            // Create a new TCP client to connect to the server with the specified IP and port
            using (TcpClient client = new TcpClient(serverIP, port))
            {   
                // Get the network stream associated with the client to send and receive data.
                using (NetworkStream stream = client.GetStream())
                {
                    Debug.Log("Connected to server");

                    while (true) // Start an infinite loop to continuously read data from the server.
                    {
                        byte[] data = new byte[61440]; // Create a new byte array to hold the received data

                        try
                        {
                            Debug.Log("Waiting for data from server");
                            
                            // Read data from the network stream into the data byte array, and store the number of bytes read in the bytesRead variable.
                            int bytesRead = stream.Read(data, 0, data.Length);

                            Debug.Log("Received data from server");
                            
                            // Check if the number of bytes read is greater than 4, indicating that the received data contains the hub prefix and sensor data.
                            if (bytesRead > 4)
                            {
                                // Parse the hub prefix from the received data
                                string hubPrefix = Encoding.ASCII.GetString(data, 0, 4);
                                if (hubPrefix != "Hub1" && hubPrefix != "Hub2")
                                {
                                    Debug.Log("Unknown hub prefix: " + hubPrefix);
                                    continue;
                                }
                                Debug.Log("Received data from server: Hub prefix: " + hubPrefix + ", Bytes read: " + bytesRead);

                                // Create a new byte array to hold the received data without the prefix
                                byte[] receivedDataBytes = new byte[bytesRead - 4];
                                System.Array.Copy(data, 4, receivedDataBytes, 0, bytesRead - 4);

                                // Create a new ReceivedData object to hold the hub prefix, received data, and number of bytes read
                                ReceivedData receivedData = new ReceivedData
                                {
                                    HubPrefix = hubPrefix,
                                    Data = receivedDataBytes,
                                    BytesRead = bytesRead - 4
                                };

                                // Add the received data to the queue to be processed by the Update method
                                lock (receivedDataQueue)
                                {
                                    receivedDataQueue.Enqueue(receivedData);
                                }
                            }
                        }
                        catch (SocketException e)
                        {
                            Debug.Log("SocketException: " + e.ToString());
                            break; // Exit inner while loop and attempt to reconnect
                        }
                        catch (IOException e)
                        {
                            Debug.Log("IOException: " + e.ToString());
                            break; // Exit inner while loop and attempt to reconnect
                        }
                    }
                }
            }
        }
        catch (SocketException e)
        {
            Debug.Log("SocketException while connecting: " + e.ToString());
        }
        catch (IOException e)
        {
            Debug.Log("IOException while connecting: " + e.ToString());
        }

        Debug.Log("Disconnected. Retrying connection in 5 seconds...");
        Thread.Sleep(5000); // Wait for 5 seconds before trying to reconnect
    }
}

    // This method returns the local IP address of the device
    private string GetLocalIPAddress()
    {
        string localIP;
        using (Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, 0))
        {
            socket.Connect("10.255.255.255", 1);
            IPEndPoint endPoint = socket.LocalEndPoint as IPEndPoint;
            localIP = endPoint.Address.ToString();
        }
        return localIP;
    }
}