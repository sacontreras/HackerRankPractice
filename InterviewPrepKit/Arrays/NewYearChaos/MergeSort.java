import java.util.Scanner;

public class MergeSort {

   /* Define your method here */
   
   // NOTE to instructor:
   //    This is from an old assignment of mine from my own implementation of MergeSort
   //    This is my own code and is at least two years old.
   
   private static void sortMerge(int[] ary, int lbound, int leftpartEnd, int rbound) {
		//pivot on left partition first
		int inspectPos = lbound;
		int rightpartPos = leftpartEnd+1;
		
		while (inspectPos < leftpartEnd+1) {
			if (ary[inspectPos] > ary[rightpartPos]) {	//then item in left partition is greater than item in right partition
				//so swap items
				int swap = ary[inspectPos];
				ary[inspectPos] = ary[rightpartPos];
				ary[rightpartPos] = swap;	
			}
			if (rightpartPos < rbound)
				rightpartPos++;
			else {
				inspectPos++;
				rightpartPos = leftpartEnd+1;
			}
		}
		
		//now reconcile right partition
		inspectPos = leftpartEnd+1;
		rightpartPos = leftpartEnd+2;
		while (inspectPos < rbound) {
			if (ary[inspectPos] > ary[rightpartPos]) {
				//so swap items
				int swap = ary[inspectPos];
				ary[inspectPos] = ary[rightpartPos];
				ary[rightpartPos] = swap;	
			} 
			if (rightpartPos < rbound)
				rightpartPos++;
			else {
				inspectPos++;
				rightpartPos = inspectPos+1;
			}
		}
	}
	
	//this function applies Divide and Conquer
	private static void mergeSort(int[] ary, int lbound, int rbound) {
		//this is a recursive function, so we need a base case
		if (lbound == rbound)	//then we have sub-divided ary until the point that the current sub-array contains only a single element
			return;
			
		//otherwise, sub-divide ary,	
		//e.g. {74, 4, -12, 8, 9, 7, 2, 0}		should produce the following logical subdivisions
		//		  |				 |
		//{-74, 4, -12, 8}	{9, 7, 2, 0}
		//	  |   	   |	  |		  |
		//{-74, 4} {-12, 8}	 {9, 7}   {2, 0}
		//  |    |   |    |   |   |    |  |
		//{-74} {4} {-12} {8} {9} {7} {2} {0}
		
		//first step is to find the index that will sub-divide ary into two logical partitions
		int lpartEnd = (lbound + rbound)/2;	//note that since this is an int, we will implicitly round down
		
		//now recursively partition ary into left and right sub-arrays
		//left partition will consist of elements from ary ranging from indexes lbound to lpartEnd
		mergeSort(ary, lbound, lpartEnd);
		//right partition will consist of elements from ary ranging from indexes lpartEnd+1 to rbound
		mergeSort(ary, lpartEnd+1, rbound);
		
		//now we need to sort/merge the left and right partitions
		sortMerge(ary, lbound, lpartEnd, rbound);
	}
	
	public static void sortArray(int[] myArr, int arrSize) {
	   mergeSort(myArr, 0, arrSize-1);
	}


   public static void main(String[] args) {
      /* Type your code here. */
         Scanner scnr = new Scanner(System.in);
         int n_ints = scnr.nextInt();
         int[] i_arr = new int[n_ints];
         
         for (int i = 0; i < n_ints; i++) {
            i_arr[i] = scnr.nextInt();
         }
         
         sortArray(i_arr, i_arr.length);
         
         for (int i = 0; i < n_ints; i++) {
            System.out.printf("%d ", i_arr[i]);
         }
         System.out.println();
   }
}