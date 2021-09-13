package SensorCenter.src;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class ServerManager extends Object{

    public ServerSocket serv;

    public byte[] sensorCode;

    public ArrayList<Connection> connections;

    public int numSensors;

    public ServerManager(int n){
        numSensors = n;
        connections = new ArrayList<>();
        sensorCode = new byte[] {-2, 68, 0, 8, 2, -97, 37}; //0xFE 0x44 0x00 0x08 0x02 0x9f 0x25
    }

    public void openServer() throws IOException {
        serv = new ServerSocket(12345);
        serv.setSoTimeout(10000);
        for(int i=0; i < numSensors; i++){
            try {
                Socket newSensor = null;
                newSensor = serv.accept();
                Connection newConnection = new Connection(newSensor);
                connections.add(newConnection);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public ArrayList pollAll() throws IOException {
        ArrayList<Byte> sensorData = new ArrayList<>();
        for(Connection c : connections)
            sensorData.add(c.poll());
        return sensorData;
    }



    public class Connection extends Object {
        public Socket connection;
        public InputStream in;
        public OutputStream out;

        public Connection(Socket s) throws IOException {
            this.connection = s;
            this.out = connection.getOutputStream();
            this.out.flush();
            this.in = connection.getInputStream();
        }

        public byte poll() throws IOException {
            out.write(sensorCode);
            byte[] input = new byte[10];
            in.read(input);
            for (byte b : input)
                System.out.println(b);
            return 0;

        }

    }

    public static void main(java.lang.String[] args) throws IOException {
        ServerManager sm = new ServerManager(1);
        sm.openServer();
        ArrayList<Byte> sensorData = sm.pollAll();
        for(Byte i : sensorData)
            System.out.print(i);



    }

}
