package hw2;

import com.google.common.collect.Lists;
import com.google.common.collect.Sets;

import java.util.*;
import java.util.List;
import java.util.concurrent.*;


public class MainTester {

    public static int NUM_THREADS = 5000;
    public static int THREAD_POOL_SIZE = 100;
    public static int WAIT_MS_LOWER_BOUND = 0;
    public static int WAIT_MS_UPPER_BOUND = 3;
    public static int TIMEOUT_MS = NUM_THREADS*WAIT_MS_UPPER_BOUND+1000;

    public static Random random = new Random(1837837);

    public static boolean printExceptions = false;
    public static boolean debugPrint = false;

    public static class Hw2Checker {

        int[] threads = new int[NUM_THREADS];
        ArrayList<ArrayList<Boolean>> activeStudyGroups;
        ArrayList<Integer> labCounts;
        ArrayList<Integer> labCapacities;
        boolean implementationFailure = false;

        public Hw2Checker(ArrayList<Integer> labCapacities, ArrayList<Integer> numStudyGroups) {
            this.labCapacities = labCapacities;

            labCounts = new ArrayList<>();
            for(int labCapacity : labCapacities)
                labCounts.add(0);

            activeStudyGroups = new ArrayList<>();
            for(int i = 0; i < labCounts.size(); i++) {
                activeStudyGroups.add(new ArrayList<>());
                for(int j = 0; j < numStudyGroups.get(i); j++) {
                    activeStudyGroups.get(i).add(false);
                }
            }

        }

        public synchronized void logEntry(int threadID, int studyGroupID, int labID) {

            //thread active and entered critical section
            threads[threadID] = 1;

            if(debugPrint) {
                System.out.println(String.format("threadID %d studyGroup %d lab %d entered", threadID, studyGroupID, labID));
                for (int i = 0; i < labCounts.size(); i++) {
                    System.out.print(String.format("Lab %d count: %d - Study Groups: ", i, labCounts.get(i)));
                    System.out.println(activeStudyGroups.get(i));
                }
            }

            //check exclusivity of StudyGroups
            for(int i = 0; i < activeStudyGroups.get(labID).size(); i++) {
                if(i != studyGroupID && activeStudyGroups.get(labID).get(i)) {
                    implementationFailure = true;
                    throw new RuntimeException("Implementation Error");
                }
            }

            activeStudyGroups.get(labID).set(studyGroupID, true);

            labCounts.set(labID, labCounts.get(labID)+1);
            if(labCounts.get(labID) > labCapacities.get(labID)) {
                implementationFailure = true;
                throw new RuntimeException("Implementation Error");
            }
        }

        public synchronized void logExit(int threadID, int studyGroupID, int labID) {

            if(debugPrint) {
                System.out.println(String.format("threadID %d studyGroup %d lab %d left", threadID, studyGroupID, labID));
                for (int i = 0; i < labCounts.size(); i++) {
                    System.out.print(String.format("Lab %d count: %d - Study Groups: ", i, labCounts.get(i)));
                    System.out.println(activeStudyGroups.get(i));
                }
            }

            //thread leaving critical section
            if(threads[threadID] != 1) {
                implementationFailure = true;
                throw new RuntimeException("Implementation Error");
            }
            threads[threadID] = 2;

            labCounts.set(labID, labCounts.get(labID)-1);
            if(labCounts.get(labID) < 0) {
                implementationFailure = true;
                throw new RuntimeException("Implementation Error");
            }
            else if(labCounts.get(labID) == 0)
                activeStudyGroups.get(labID).set(studyGroupID, false);
        }

        public synchronized void logTerminate(int threadID) {
            if(threads[threadID] != 2) {
                implementationFailure = true;
                throw new RuntimeException("Implementation Error");
            }

            threads[threadID] = 3;
        }

        public boolean finalFailCheckup() {
            for(int threadCode : threads)
                if(threadCode != 3)
                    return false;
            return !implementationFailure;
        }


    }

    public static boolean test(ArrayList<Integer> labCapacities, ArrayList<Integer> numStudyGroups)
    {
        ArrayList<Lab> labs = new ArrayList<>();
        for(int i = 0; i < labCapacities.size(); i++) {
            labs.add(new Lab(Integer.toString(i), labCapacities.get(i)));
        }

        ArrayList<ArrayList<StudyGroup>> studyGroups = new ArrayList<>();
        for(int i = 0; i < labs.size(); i++) {
            studyGroups.add(new ArrayList<>());
            for(int j = 0; j < numStudyGroups.get(i); j++) {
                studyGroups.get(i).add(new StudyGroup(i+"_"+j, labs.get(i)));
            }
        }

        Hw2Checker checker = new Hw2Checker(labCapacities, numStudyGroups);

        ExecutorService threadPoolExecutor = Executors.newFixedThreadPool(THREAD_POOL_SIZE);


        for(int threadID = 0; threadID < NUM_THREADS; threadID++) {

            final int labID = random.nextInt(labCapacities.size());
            final int studyGroupID = random.nextInt(numStudyGroups.get(labID));
            final int millis = WAIT_MS_LOWER_BOUND+random.nextInt(WAIT_MS_UPPER_BOUND-WAIT_MS_LOWER_BOUND);

            int finalThreadID = threadID;
            threadPoolExecutor.execute(() -> {
                try{
                    //STUDENT BODY
                    StudyGroup studyGroup = studyGroups.get(labID).get(studyGroupID);

                    studyGroup.startStudyingWith();
                        checker.logEntry(finalThreadID, studyGroupID, labID);

                        try {
                            Thread.sleep(millis);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            throw new RuntimeException(e);
                        }

                        checker.logExit(finalThreadID, studyGroupID, labID);
                    studyGroup.stopStudyingWith();

                    checker.logTerminate(finalThreadID);

                }
                catch(Exception e) {
                    Thread.currentThread().interrupt();
                    if(printExceptions)
                        e.printStackTrace();
                }

            });
        }

        threadPoolExecutor.shutdown();
        try {
            if(!threadPoolExecutor.awaitTermination(TIMEOUT_MS, TimeUnit.MILLISECONDS)) {
                threadPoolExecutor.shutdownNow();
                return false;
            }
        }
        catch (InterruptedException ie) {
            threadPoolExecutor.shutdownNow();
            Thread.currentThread().interrupt();
            throw new RuntimeException(ie);
        }

        return checker.finalFailCheckup();
    }

    public static void main(String[] args) {

        System.out.printf("\n STUDENT_ID: %s \n", args[0]);
        printExceptions = Integer.parseInt(args[1]) == 1;
        debugPrint = Integer.parseInt(args[2]) == 1;

        //lock mode
        System.out.printf("\n LOCK_MODE_SCORE: %d \n",
                test(new ArrayList<>(List.of(1)), new ArrayList<>(List.of(1)))?1:0);

        //semaphore mode
        int kid_mode_success = 0;
        for(int i = 2; i < 4; i++) {
            kid_mode_success += test(new ArrayList<>(List.of(i)), new ArrayList<>(List.of(1)))?1:0;
        }
        System.out.printf("\n SEMAPHORE_MODE_SCORE: %d \n", kid_mode_success);

        //single lab mode
        int normal_mode_success = 0;
        for(int cap = 1; cap < 4; cap++) {
            for(int numGroups = 2; numGroups < 4; numGroups++) {
                normal_mode_success += test(new ArrayList<>(List.of(cap)), new ArrayList<>(List.of(numGroups)))?1:0;
            }
        }
        System.out.printf("\n NORMAL_MODE_SCORE: %d \n", normal_mode_success);

        //double lab mode
        List<List<Integer>> capacities = Lists.cartesianProduct(List.of(1,2,3), List.of(1,2,3));
        Set<Set<Integer>> groupNumCombinations = Sets.combinations(Set.of(1,2,3),2);

        int double_lab_success = capacities.stream().mapToInt(
                cap -> groupNumCombinations.stream().mapToInt(
                        groupNum -> test(new ArrayList<>(cap), new ArrayList<>(groupNum))?1:0).sum()).sum();

        System.out.printf("\n DOUBLE_LAB_SCORE: %d \n", double_lab_success);

    }

}
