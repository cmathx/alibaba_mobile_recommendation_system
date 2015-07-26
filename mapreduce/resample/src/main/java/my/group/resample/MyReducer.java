package my.group.resample;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.Reducer;

import java.io.IOException;
import java.util.Iterator;

/**
 * Reducer模板。请用真实逻辑替换模板内容
 */
public class MyReducer implements Reducer {
	private Record result;

	public void setup(TaskContext context) throws IOException {
		result = context.createOutputRecord();
	}

	public void reduce(Record key, Iterator<Record> values, TaskContext context)
			throws IOException {
		while (values.hasNext()) {
			Record val = values.next();
			
			result.set(0, key.getString("user_id"));
			result.set(1, key.getString("item_id"));
			result.set(2, val.getDouble("view_rate"));
			result.set(3, val.getDouble("col_rate"));
			result.set(4, val.getDouble("cart_rate"));
			result.set(5, val.getDouble("buy_rate"));
	    	for(int i = 0; i < 24; ++i){
	    		String prefix = "view_occur";
	    		result.setBigint(6 + i, val.getBigint(prefix + Integer.toString(i + 1)));
	    	}
	    	for(int i = 0; i < 3; ++i){
	    		String prefix = "ccb_occur";
	    		result.set(30 + i, val.getBigint(prefix + Integer.toString(i + 1)));
	    	}
	    	result.set(33, val.getBigint("view_col"));
	    	result.set(34, val.getBigint("view_cart"));
	    	for(int i = 0; i < 7; ++i){
	    		String prefix = "behavior_cnt";
	    		result.set(35 + i, val.getDouble(prefix + Integer.toString(i + 1)));
	    	}
	    	for(int i = 0; i < 4; ++i){
	    		String prefix = "focus_cnt";
	    		result.set(42 + i, val.getDouble(prefix + Integer.toString(i + 1)));
	    	}
	    	result.set(46, val.getBigint("is_buy"));
			int is_buy = Integer.valueOf(String.valueOf(val.getBigint("is_buy")));
			if (is_buy == 1) {
				int resample_cnt = 40;
				for (int i = 0; i < resample_cnt; ++i)
					context.write(result);
			} else
				context.write(result);
		}
	}

	public void cleanup(TaskContext arg0) throws IOException {

	}
}
