import java.io.FileReader;
import java.util.HashMap;
import java.util.regex.Pattern;
import java.io.*;

/**
 * Created by laceyliu on 4/4/15.
 */
public class nb {
    public HashMap<String, HashMap<String, Double>> prob_map;
    public HashMap<String, Double> p_v;
    public String dir = "data/";
    //public String dir = "";
    public HashMap<String, Integer> vocab;

    public nb(){
        this.prob_map = new HashMap<String, HashMap<String, Double>>();
        this.p_v = new HashMap<String, Double>();
        this.vocab = new HashMap<String, Integer>();
    }

    public void learn_naiveBayes(String train_path) throws IOException {
        HashMap<String, Integer> length_map = new HashMap<String, Integer>();
        HashMap<String, Integer> cnt_map = new HashMap<String, Integer>();

        HashMap<String, HashMap<String, Integer>> word_map = new HashMap<String, HashMap<String, Integer>>();
        HashMap<String, Integer> dummy = new HashMap<String, Integer>();
        HashMap<String, Integer> dummy2 = new HashMap<String, Integer>();
        word_map.put("C", dummy);
        word_map.put("L", dummy2);

        // read in all blogs in train_set
        BufferedReader scan = new BufferedReader(new FileReader(train_path));
        String blog = null;
        int blog_cnt = 0;
        while((blog = scan.readLine())!= null){

            //|Examples|
            blog_cnt += 1;

            //label for each doc
            String label = "";
            if (Pattern.matches("con.*", blog)){
                label = "C";
            }else{
                label = "L";
            }

            //|docs|
            if (cnt_map.containsKey(label)){
                cnt_map.put(label, cnt_map.get(label)+1);
            }else{
                cnt_map.put(label, 1);
            }

            // read in all tokens in each blog
            BufferedReader scan_content = new BufferedReader(new FileReader(dir+blog));
            String token = null;
            while((token = scan_content.readLine())!= null){
                token = token.toLowerCase();
                //global vocabulary
                if (this.vocab.containsKey(token)){
                    this.vocab.put(token, this.vocab.get(token)+1);
                }else{
                    this.vocab.put(token, 1);
                }

                //label -> n
                if (length_map.containsKey(label)){
                    length_map.put(label, length_map.get(label)+1);
                }else{
                    length_map.put(label, 1);
                }

                //label -> word k-> n_k
                if (word_map.get(label).containsKey(token)){
                    word_map.get(label).put(token, word_map.get(label).get(token)+1);
                }else{
                    word_map.get(label).put(token, 1);
                }
            }
            scan_content.close();
        }

        //calculate p_v
        for (String label : cnt_map.keySet()){
            double prob = Math.log(1.0 * cnt_map.get(label) / blog_cnt);
            this.p_v.put(label, prob);
        }

        //calculate prob(w|v)
        for (String label: length_map.keySet()){
            HashMap<String, Double> tmp = new HashMap<String, Double>();
            for (String word : vocab.keySet()){
                double n_k = 0.0;
                if (word_map.get(label).containsKey(word)){
                    n_k = word_map.get(label).get(word);
                }
                double n = length_map.get(label);
                double prob = Math.log((n_k + 1.0)/(n + this.vocab.size()));
                tmp.put(word, prob);
            }
            this.prob_map.put(label, tmp);
        }
        scan.close();
        return;

    }

    public double classify_naiveBayes(String test_path) throws IOException {
        int hit = 0;

        BufferedReader scan = new BufferedReader(new FileReader(test_path));
        String blog = null;
        int blog_cnt = 0;
        while((blog = scan.readLine())!= null){
            String act_label = "";
            if (blog.contains("con")) {
                act_label = "C";
            }else {
                act_label = "L";
            }

            String max_label = "nil";
            double prob_c = 0.0;
            double prob_l = 0.0;
            BufferedReader scan_content = new BufferedReader(new FileReader(dir + blog));
            String token = "";
            while ((token = scan_content.readLine())!= null){
                token = token.toLowerCase();
                if (vocab.containsKey(token)) {
                    prob_c += this.prob_map.get("C").get(token);
                    prob_l += this.prob_map.get("L").get(token);
                }else{
                    continue;
                }
            }

            prob_c += this.p_v.get("C");
            prob_l += this.p_v.get("L");

            if (prob_c > prob_l){
                max_label = "C";
            }else{
                max_label = "L";
            }

            if (max_label.equals(act_label)){
                hit += 1;
            }

            System.out.println(max_label);
            blog_cnt += 1;
        }

        double acc = 1.0*hit/ blog_cnt;

        return acc;

    }

    static public void main(String[] args) throws IOException {
        nb nb = new nb();
        nb.learn_naiveBayes(nb.dir+args[0]);
        double acc = nb.classify_naiveBayes(nb.dir+args[1]);
        System.out.println("Accuracy: " + String.format("%.4f",acc));
    }
}
