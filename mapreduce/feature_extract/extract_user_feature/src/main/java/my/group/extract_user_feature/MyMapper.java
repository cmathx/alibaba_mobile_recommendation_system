package my.group.extract_user_feature;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.Mapper;

import java.io.IOException;

/**
 * Mapper模板。请用真实逻辑替换模板内容
 */
public class MyMapper implements Mapper {
	private Record key;
    private Record value;

    public void setup(TaskContext context) throws IOException {
    	key = context.createMapOutputKeyRecord();
        value = context.createMapOutputValueRecord();
    }

    public void map(long recordNum, Record record, TaskContext context) throws IOException {
    	key.setString("user_id", record.getString(0));
    	value.setString("item_id", record.getString(1));
    	value.setString("time", record.getString(5));
    	value.setString("behavior_type", String.valueOf(record.getBigint(2)));
        context.write(key, value);
    }

    public void cleanup(TaskContext context) throws IOException {

    }
}