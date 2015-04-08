/**
 * Created by laceyliu on 4/5/15.
 */

import java.util.*;
import java.io.*;

public class topwords {

    public HashMap<String, HashMap<String, Double>> word_score;
    public List<String> labels;

    //public String dir = "data/";
    public String dir = "";

    public topwords(){
        this.word_score = new  HashMap<String, HashMap<String, Double>>();
        this.labels = new ArrayList<String>();
        this.labels.add("L");
        this.labels.add("C");
    }

    public List sortByValue(final Map m) {
        List keys = new ArrayList();
        keys.addAll(m.keySet());
        Collections.sort(keys, new Comparator() {
            public int compare(Object o1, Object o2) {
                Object v1 = m.get(o1);
                Object v2 = m.get(o2);
                if (v1 == null) {
                    return (v2 == null) ? 1 : 0;
                }
                else if (v1 instanceof Comparable) {
                    return -((Comparable) v1).compareTo(v2);
                }
                else {
                    return 1;
                }
            }
        });
        return keys;
    }

    public void calculateConditionalProb(String path) throws IOException {
        HashMap<String, Integer> n_map = new HashMap<String, Integer>();
        HashMap<String, Integer> docs_map = new HashMap<String, Integer>();
        HashMap<String, Integer>vocab = new HashMap<String, Integer>();

        HashMap<String, HashMap<String, Integer>> nk_map = new HashMap<String, HashMap<String, Integer>>();
        HashMap<String, Integer> c_nk = new HashMap<String, Integer>();
        HashMap<String, Integer> l_nk = new HashMap<String, Integer>();
        nk_map.put("C", c_nk);
        nk_map.put("L", l_nk);

        String blogPath = null;
        int example = 0;
        BufferedReader scan = new BufferedReader(new FileReader(this.dir+path));
        int blog_cnt = 0;
        while((blogPath = scan.readLine())!= null){

            String label = "";

            //label
            if (blogPath.contains("con")){
                label = "C";
            }else{
                label = "L";
            }

            //|docs|
            if (docs_map.containsKey(label)){
                docs_map.put(label, docs_map.get(label)+1);
            }else{
                docs_map.put(label, 1);
            }

            BufferedReader scan_content = new BufferedReader(new FileReader(dir+blogPath));
            String token = null;
            while((token = scan_content.readLine())!= null){
                token = token.toLowerCase();

                //n
                if (n_map.containsKey(label)){
                    n_map.put(label, n_map.get(label)+1);
                }else{
                    n_map.put(label, 1);
                }

                //vocab
                if (vocab.containsKey(token)){
                    vocab.put(token, vocab.get(token)+1);
                }else{
                    vocab.put(token, 1);
                }

                //n_k
                if (nk_map.get(label).containsKey(token)){
                    nk_map.get(label).put(token, nk_map.get(label).get(token)+1);
                }else{
                    nk_map.get(label).put(token, 1);
                }
            }

            example += 1;
        }

        //p_v
        for (String label : docs_map.keySet()){
            double prob = Math.log(1.0 * docs_map.get(label) / example);
        }

        //p(w|v)
        for (String label: n_map.keySet()){
            HashMap<String, Double> tmp = new HashMap<String, Double>();
            for (String term: vocab.keySet()){
                double n_k = 0.0;
                if (nk_map.get(label).containsKey(term)){
                    n_k = nk_map.get(label).get(term);
                }
                double prob = Math.log((n_k + 1.0)/(n_map.get(label) + vocab.size()));
                tmp.put(term, prob);
            }
            this.word_score.put(label, tmp);
        }

        return;

    }

    public static void main(String args[]) throws IOException {
        String trainPath = args[0];

        topwords topwords = new topwords();

        topwords.calculateConditionalProb(trainPath);


        for (String label : topwords.labels){

            HashMap<String, Double> scoreMap = topwords.word_score.get(label);
            List<String> top_words = topwords.sortByValue(scoreMap);

            int cnt = 0;

            for (String word : top_words){
                String score = String.format("%.04f", Math.exp(scoreMap.get(word)));
                System.out.println(word + " " + score);
                cnt += 1;
                if (cnt >= 20){
                    break;
                }
            }
            System.out.println();
        }
    }
}
