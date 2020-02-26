import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Vector;

public class bikes {
    public static void main(String[] args) {
        ArrayList<Integer> B = new ArrayList<>(Arrays.asList(10,0,8,2,-1,12,11,3));
        //ArrayList<Integer> B = new ArrayList<>(Arrays.asList(5,8,2,10,14,7,3,6,11));
        //ArrayList<Integer> B = new ArrayList<>(Arrays.asList(5,5,6,1,89,34,12,119,56,78,99));
        ArrayList<Integer> C = new ArrayList<>();

        int max;
        int max_rel;

        Collections.sort(B);

        for(int i = 0; i < B.size(); i++){
            int a;
                if(i < (B.size() - 1)){
                    a = B.get(i+1) - B.get(i);
                    C.add(a);
                }
                else{
                    break;
                }
        }

        max = Collections.max(C);
        max_rel = max/2;
        System.out.print(max_rel);
    }
}
