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

    void Awake()
    {
        // Set the path to the folder where you want to save the CSV files
        saveFolderPath = Application.dataPath + "/data/";
        Directory.CreateDirectory(saveFolderPath);
    }

    // Set the CSV file name and increment counter
    private string fileName = "sensor_data_";
    private int fileCounter = 0;

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
                        if (bytesRead > 0)
                        {
                            // If the file stream is not null, close it
                            FileStream fileStream = null;

                            // Create a new CSV file with an incremented file name
                            string filePath = Path.Combine(saveFolderPath, fileName + fileCounter.ToString() + ".csv");
                            Debug.Log("Saving data to file: " + filePath);
                            fileStream = new FileStream(filePath, FileMode.CreateNew, FileAccess.Write);

                            // Write the data to the CSV file
                            fileStream.Write(data, 0, bytesRead);

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
