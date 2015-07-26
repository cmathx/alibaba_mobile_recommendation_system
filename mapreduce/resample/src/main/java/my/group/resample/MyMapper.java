package my.group.resample;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.Mapper;

import java.io.IOException;

/**
 * Mapper模板。请用真实逻辑替换模板内容
 */
public class MyMapper implements Mapper {
	private Record result;

    public void setup(TaskContext context) throws IOException {
//    	key = context.createMapOutputKeyRecord();
//        value = context.createMapOutputValueRecord();
    	result = context.createOutputRecord();
    }

    public void map(long recordNum, Record record, TaskContext context) throws IOException {
<<<<<<< HEAD
    	long is_buy = record.getBigint(112);
    	for(int i = 0; i <= 112; ++i)
=======
    	long is_buy = record.getBigint(148);
    	for(int i = 0; i <= 148; ++i)
>>>>>>> 2caa16d7f0e44e101ad6d3f0581509e0e94c5181
    		result.set(i, record.get(i));
    	
    	//添加交叉特征
    	
    	
    	if(is_buy == 0)
    		context.write(result);
    	else{
    		int resample_cnt = 40;
    		for(int i = 0; i < resample_cnt; ++i)
    			context.write(result);
    	}
    }

    public void cleanup(TaskContext context) throws IOException {

    }
} 
