import java.io.*;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;

/**
 * The class <code>Solver</code> is an implementation of a greedy algorithm to solve the knapsack problem.
 *
 */
public class Solver {
    
    /**
     * The main class
     */
    public static void main(String[] args) {
        // skipped ks_82_0, ks_106_0, ks_300_0
        String[] someFiles = new String[] {"ks_4_0", "ks_19_0", "ks_30_0", "ks_40_0", "ks_45_0", "ks_50_0", "ks_50_1", "ks_60_0", "ks_100_0", "ks_100_1", "ks_100_2", "ks_200_0", "ks_200_1", "ks_300_0", "ks_400_0", "ks_500_0", "ks_1000_0", "ks_10000_0"};
        try {
            solve(args);

            /*int sum = 0;
            for (String s : someFiles) {
                System.out.println("\n" + s);
                sum += solve(new String[] {"-file=./data/" + s, "DONOTPRINT"});
            }*/
            //System.out.println("\nTOTAL VALUE: " + sum/105124029.);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    /**
     * Read the instance, solve it, and print the solution in the standard output
     */
    public static int solve(String[] args) throws IOException {
        String fileName = null;

        boolean print = true;

        // get the temp file name
        for(String arg : args){
            if(arg.startsWith("-file=")){
                fileName = arg.substring(6);
            }
            if (arg.equals("DONOTPRINT")) {
                print = false;
            }
        }
        if(fileName == null)
            return -999999999;

        // read the lines out of the file
        List<String> lines = new ArrayList<String>();

        BufferedReader input =  new BufferedReader(new FileReader(fileName));
        try {
            String line = null;
            while (( line = input.readLine()) != null){
                lines.add(line);
            }
        }
        finally {
            input.close();
        }
        
        
        // parse the data in the file
        String[] firstLine = lines.get(0).split("\\s+");
        int items = Integer.parseInt(firstLine[0]);
        int capacity = Integer.parseInt(firstLine[1]);

        int[] values = new int[items];
        int[] weights = new int[items];

        for(int i=1; i < items+1; i++){
          String line = lines.get(i);
          String[] parts = line.split("\\s+");

          values[i-1] = Integer.parseInt(parts[0]);
          weights[i-1] = Integer.parseInt(parts[1]);
        }


        double[] fillValues = new double[values.length];
        for (int i = 0; i < values.length; i++) {
            fillValues[i] = values[i] / (double) weights[i];
        }
        Integer[] fillIndices = new Integer[values.length];
        int runningIndex = 0;
        while (true) {
            int indexMax = -10;
            double valueMax = -10;
            for (int i = 0; i < values.length; i++) {
                if (fillValues[i] >= valueMax) {
                    valueMax = fillValues[i];
                    indexMax = i;
                }
            }

            if (valueMax == -1) {
                break;
            }

            fillIndices[indexMax] = runningIndex++;
            fillValues[indexMax] = -1;
        }
        int[] argsortInd = new int[values.length];
        for (int i = 0; i < values.length; i++) {
            argsortInd[i] = Arrays.asList(fillIndices).indexOf(i);
        }

        int[] weightsRO = new int[argsortInd.length];
        int[] valuesRO = new int[argsortInd.length];
        for (int i = 0; i < argsortInd.length; i++) {
            weightsRO[i] = weights[argsortInd[i]];
            valuesRO[i] = values[argsortInd[i]];
        }

        SolveActual solver = new SolveActual();
        long startTime = System.nanoTime();
        Solution s = solver.solve(new Solution(0, 0, new int[values.length], 0), valuesRO, weightsRO, capacity);
        long endTime = System.nanoTime();

        if (!print) {
            System.out.println("time: " + (endTime - startTime) / 1000 + ", result: " + s.value);
        }

        int value = s.value;
        int weight = s.weight;
        int[] taken = new int[weights.length];

        for (int i = 0; i < weights.length; i++) {
            taken[argsortInd[i]] = s.taken[i];
        }

        if (print) {
            // prepare the solution in the specified output format
            System.out.println(value + " 1");
            for (int i = 0; i < items; i++) {
                System.out.print(taken[i] + " ");
            }
            System.out.println("");
        }
        return value;
    }
}