import java.util.Arrays;

public class SolveActual {

    int bestFoundSolution = 0;

    public Solution solve(Solution solution, int[] values, int[] weights, int K) {
        //System.out.println(Arrays.toString(solution.taken) + " | " + solution.n + " : " + bestFoundSolution);
        if (solution.n == values.length) {
            if (solution.value > bestFoundSolution) {
                bestFoundSolution = solution.value;
            }
            return solution;
        }


        double bestFiller = (values[0]/ (double) weights[0]);
        if (solution.value + bestFiller*(K-solution.weight) <= bestFoundSolution) {
            //System.out.println("prune1");
            return solution;
        }

        //System.out.println("BEST FIL" + solution.value + bestFiller*remainingSpace + "  GURP " + bestFoundSolution);

        if (true) {
            int propWeight = solution.weight;
            int propValue = solution.value;

            for (int i = solution.n; i < values.length; i++) {
                if (propWeight + weights[i] <= K) {
                    propWeight += weights[i];
                    propValue += values[i];
                }
            }

            int remainingSpace = K - propWeight;
            propValue += bestFiller * remainingSpace;


            if (propValue <= bestFoundSolution) {
                //System.out.println("prune2");
                return solution;
            }
        }


        /*Solution s1 = null;
        boolean randomizedOrder = false;
        if (Math.random() < 0) {
            s1 = solve(new Solution(solution.value, solution.weight, solution.taken, solution.n+1), values, weights, K, argsortInd);
            randomizedOrder = true;
        }*/

        Solution s2 = null;
        if (solution.weight + weights[solution.n] < K) {
            int[] taken = solution.taken.clone();
            taken[solution.n] = 1;
            s2 = solve(new Solution(solution.value+values[solution.n], solution.weight+weights[solution.n], taken, solution.n+1), values, weights, K);
        }
        /*if (!randomizedOrder) {
            s1 = solve(new Solution(solution.value, solution.weight, solution.taken, solution.n+1), values, weights, K, argsortInd);
        }*/
        Solution s1 = solve(new Solution(solution.value, solution.weight, solution.taken, solution.n+1), values, weights, K);


        if (s2 == null) {
            return s1;
        } else {
            if (s2.value > s1.value) {
                return s2;
            } else {
                return s1;
            }
        }
    }

}
