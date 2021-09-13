import java.util.*;
import java.io.*;

public class SensorCenter {
    public ArrayList<ArrayList<Integer>> values;
    private int runtime;
    private int pollFrequency;
    private String fileName;
    private StringBuffer written;


    //Termination values
    public static int SUCCESS = 0;
    public static int FAIL  = -1;

    /**
     * Sensor Center is in charge of all the information dealing with initializaion
     * @param run   How much time the data is going to be collected for
     * @param freq  how often the data is collected within the run
     * @param file  File name to output to CSV
     */
    public SensorCenter( int run, int freq, String file )
    {
            runtime = run;
            pollFrequency = freq;
            fileName = file;
            values = new ArrayList<>();
            written = new StringBuffer("");
    }


    public int start() {
        return 0;
    }

    /**
     * Exports the double ArrayList of values to .csv
     * @return SUCCESS if completed or FAIL if error detected
     */
    public int export() {
        try {
                BufferedWriter fileWriter = new BufferedWriter( new FileWriter( fileName ) );
                int row = 1;

                for(ArrayList<Integer> intArr : values)
                {
                    Integer last = intArr.get(intArr.size()-1);
                    written.append(row);
                    written.append(",");
                    for(Integer value : intArr)
                    {
                        written.append(value);
                        if(!value.equals(last))
                         written.append(",");
                    }
                    written.append("\n");
                    row++;
                }
                fileWriter.write( written.toString() );
                fileWriter.close();
            }
         catch (IOException e) {
            System.out.println( "File IO error:" );
            e.printStackTrace();
            return FAIL;
        }
        return SUCCESS;
    }


    /**
     * Main running element for the class
     * Change boolean to true if test is to be ran available
     * @param args Arguments from the command line
     */
    public static void main (String[] args)
    {
        //boolean test = true;
        if (args.length != 3)
        {
            System.out.println("Invalid number of arguments");
            System.exit(FAIL);
        }

        int time = Integer.parseInt(args[0]);
        int frequency = Integer.parseInt(args[1]);
        String fileName = args[2];
        SensorCenter sens = new SensorCenter(time, frequency, fileName);
        for (int i = 0; i < 10; i++) {
            sens.values.add(new ArrayList<>());
            for (int x = 0; x < 10; x++) {
                sens.values.get(i).add(x);
            }
        }
        sens.export();

    }


}
