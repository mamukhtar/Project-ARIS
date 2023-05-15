using UnityEngine;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.IO;

public class UnityClientScript_csv : MonoBehaviour
{
    // Set the server's IP address and port
    private string serverIP = "10.0.0.173";
    private int port = 8000;

    private string saveFolderPath;

    // Set the CSV file name
    private string fileName = "sensor_data_";
    private int fileCounterHub1 = 0;
    private int fileCounterHub2 = 0;


    // Start is called before the first frame update
    void Start()
    {
        // Create a new thread for connecting to the server and receiving data
        Thread clientThread = new Thread(new ThreadStart(ClientThread));
        clientThread.Start();
    }

    // ClientThread method for connecting to the server and receiving data
   void ClientThread()
    {
        Debug.Log("Starting ClientThread");
        while (true)
        {
            using (TcpClient client = new TcpClient(serverIP, port))
            {
                using (NetworkStream stream = client.GetStream())
                {
                    byte[] data = new byte[61440];

                    try
                    {
                        Debug.Log("Waiting for data from server");

                        int bytesRead = stream.Read(data, 0, data.Length);

                        Debug.Log("Received data from server");

                        if (bytesRead > 4)
                        {
                            string hubPrefix = Encoding.ASCII.GetString(data, 0, 4);
                            if (hubPrefix != "Hub1" && hubPrefix != "Hub2")
                            {
                                Debug.Log("Unknown hub prefix: " + hubPrefix);
                                continue;
                            }
                            Debug.Log("Received data from server: Hub prefix: " + hubPrefix + ", Bytes read: " + bytesRead);

                            string folderPath = hubPrefix == "Hub1" ? "Hub1_data" : "Hub2_data";
                            saveFolderPath = Path.Combine(Application.dataPath, folderPath);
                            Directory.CreateDirectory(saveFolderPath);

                            FileStream fileStream = null;

                            string filePath = Path.Combine(saveFolderPath, hubPrefix + "_" + fileName + (hubPrefix == "Hub1" ? fileCounterHub1 : fileCounterHub2) + ".csv");
                            Debug.Log("Saving data to file: " + filePath);
                            fileStream = new FileStream(filePath, FileMode.CreateNew, FileAccess.Write);

                            fileStream.Write(data, 4, bytesRead - 4);

                            if (hubPrefix == "Hub1") {
                                fileCounterHub1++;
                            } else {
                                fileCounterHub2++;
                            }

                            Debug.Log("File counter Hub1: " + fileCounterHub1 + ", File counter Hub2: " + fileCounterHub2);

                            fileStream.Close();
                        }
                    }
                    catch (SocketException e)
                    {
                        Debug.Log("SocketException: " + e.ToString());
                    }
                }
            }
        }
    }
}



































/*
    // ClientThread method for connecting to the server and receiving data
    void ClientThread()
    {
        while (true)
        {
            // Create a new TCP client socket and connect to the server
                using (TcpClient client = new TcpClient(serverIP, port))
                {
                    // Create a new network stream for receiving data
                    using (NetworkStream stream = client.GetStream())
                    {
                        // Create a byte array for receiving data
                        byte[] data = new byte[61440];

                        try
                        {
                            Debug.Log("Waiting for data from server");

                            // Read the data from the server
                            int bytesRead = stream.Read(data, 0, data.Length);

                            Debug.Log("Received data from server");

                            // If the data is not empty and the length is greater than zero, save it to a new CSV file
                            if (bytesRead > 4)
                            {
                                string hubPrefix = Encoding.ASCII.GetString(data, 0, 4);
                                if (hubPrefix != "Hub1" && hubPrefix != "Hub2")
                                {
                                    Debug.Log("Unknown hub prefix: " + hubPrefix);
                                    continue;
                                }

                                // If the file stream is not null, close it
                                FileStream fileStream = null;

                                // Create a new CSV file with an incremented file name based on the hubPrefix
                                string filePath = Path.Combine(saveFolderPath, hubPrefix + "_" + fileName + fileCounter.ToString() + ".csv");
                                Debug.Log("Saving data to file: " + filePath);
                                fileStream = new FileStream(filePath, FileMode.CreateNew, FileAccess.Write);

                                // Write the data (excluding the hub prefix) to the CSV file
                                fileStream.Write(data, 4, bytesRead - 4);

                                // Increment the file counter
                                fileCounter++;

                                // Close the file stream
                                fileStream.Close();
                            }
                        }
                    catch (SocketException e)
                    {
                        Debug.Log("SocketException: " + e.ToString());
                    }
                }
            }
        }
    }
}
  */             
