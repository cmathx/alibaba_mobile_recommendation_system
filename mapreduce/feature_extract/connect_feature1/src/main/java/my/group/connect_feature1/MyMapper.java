package my.group.connect_feature1;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.Mapper;

import java.io.IOException;

/**
 * Mapper模板。请用真实逻辑替换模板内容
 */
public class MyMapper implements Mapper {
    private Record word;
    private Record one;

    public void setup(TaskContext context) throws IOException {
        word = context.createMapOutputKeyRecord();
        one = context.createMapOutputValueRecord();
        one.setBigint(0, 1L);
    }

    public void map(long recordNum, Record record, TaskContext context) throws IOException {
    	//user_item_feature 52
    	//user_feature 39
    	//item_feature 24
    	if(record.getColumnCount() > 50){
    		
    	}
        String w = record.getString(0);
        word.setString(0, w);
        context.write(word, one);
    }

    public void cleanup(TaskContext context) throws IOException {

    }
}