package my.group.extract_item_feature;

import com.aliyun.odps.data.Record;
import com.aliyun.odps.mapred.Reducer;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

import org.codehaus.jackson.map.ser.PropertyBuilder.EmptyStringChecker;

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
		long buy_cnt = 0L, contact_cnt = 0L, buy_user_cnt = 0L, contact_user_cnt = 0L, back_user_cnt = 0L;
		long cart_cnt = 0L, cart_user_cnt = 0L, back_user_cart_cnt = 0L;
		Set<String> cart_user_set = new HashSet<String>(), buy_user_set = new HashSet<String>(), contact_user_set = new HashSet<String>();
		Map<String, Set> user_cart_time = new TreeMap<String, Set>(), user_buy_time = new TreeMap<String, Set>();
		long[] final_item_beh_hour = new long[5];
		long[] cart_users = new long[5], beh_users = new long[5], buy_users = new long[5];//最近1/3/7/15/30天被多少不同的用户交互/购买
//		long[] cart_count = new long[5], beh_count = new long[5], buy_count = new long[5];//最近1/3/7/15/30天被用户交互数/购买数
		long[] cart_days = new long[3], beh_days = new long[3], buy_days = new long[3];//最近7/15/30天有多少天被用户交互/购买
		
		boolean[] cart_day_flag = new boolean[30], beh_day_flag = new boolean[30], buy_day_flag = new boolean[30];
		for(int i = 0; i < 5; ++i)
			final_item_beh_hour[i] = 720L;
		while (values.hasNext()) {
			Record val = values.next();
			String user_id = val.getString("user_id");
			String date = val.getString("time");
			String day_str = date.substring(0, 10);
			int type = Integer.parseInt(val.getString("behavior_type")) - 1;
			long t_hour = getHourSpan("2014-12-19 00", date);
			if(t_hour <= 0 || t_hour >= 720)
				continue;
			int t_day = (int)t_hour / 24;
			if (type == 3) {
				buy_cnt++;
				buy_user_set.add(user_id);
				if (user_buy_time.containsKey(user_id)) {
					user_buy_time.get(user_id).add(day_str);
				} else {
					Set<String> t_day_set = new HashSet<String>();
					t_day_set.add(day_str);
					user_buy_time.put(user_id, t_day_set);
				}
//				if(t_hour < final_item_beh_hour[0])
//					final_item_beh_hour[0] = t_hour;
				if(t_hour < 24){
					buy_users[0]++;
				}
				if(t_hour < 72){
					buy_users[1]++;
				}
				if(t_hour < 168){
					buy_users[2]++;
				}
				if(t_hour < 360){
					buy_users[3]++;
				}
				buy_users[4]++;
				buy_day_flag[t_day] = true;
			} 
			else if(type == 2){
				cart_cnt++;
				cart_user_set.add(user_id);
				if(user_cart_time.containsKey(user_id)){
					user_cart_time.get(user_id).add(day_str);
				}
				else{
					Set<String> t_day_set = new HashSet<String>();
					t_day_set.add(day_str);
					user_cart_time.put(user_id, t_day_set);
				}
				if(t_hour < 24)
					cart_users[0]++;
				if(t_hour < 72)
					cart_users[1]++;
				if(t_hour < 168)
					cart_users[2]++;
				if(t_hour < 360)
					cart_users[3]++;
				cart_users[4]++;
				cart_day_flag[t_day] = true;
			}
//			else {
				contact_cnt++;
				contact_user_set.add(user_id);
				if(t_hour < final_item_beh_hour[type])
					final_item_beh_hour[type] = t_hour;
				if(t_hour < final_item_beh_hour[4])
					final_item_beh_hour[4] = t_hour;
				if(t_hour < 24){
					beh_users[0]++;
				}
				if(t_hour < 72){
					beh_users[1]++;
				}
				if(t_hour < 168){
					beh_users[2]++;
				}
				if(t_hour < 360){
					beh_users[3]++;
				}
				beh_users[4]++;
				beh_day_flag[t_day] = true;
//			}
		}
		cart_user_cnt  = cart_user_set.size();
		buy_user_cnt = buy_user_set.size();
		contact_user_cnt = contact_user_set.size();
		for (Map.Entry<String, Set> entry : user_buy_time.entrySet()) {
			if(entry.getValue().size() != 1)
				back_user_cnt++;
		}
		for(Map.Entry<String, Set> entry : user_cart_time.entrySet()){
			if(entry.getValue().size() != 1)
				back_user_cart_cnt++;
		}
		
		
		for(int i = 0; i < 30; ++i){
			if(i < 7){
				if(beh_day_flag[i])
					beh_days[0]++;
			}
			if(i < 15){
				if(beh_day_flag[i])
					beh_days[1]++;
			}
			if(beh_day_flag[i])
				beh_days[2]++;
		}
		
		for(int i = 0; i < 30; ++i){
			if(i < 7){
				if(buy_day_flag[i])
					buy_days[0]++;
			}
			if(i < 15){
				if(buy_day_flag[i])
					buy_days[1]++;
			}
			if(buy_day_flag[i])
				buy_days[2]++;
		}
		
		for(int i = 0; i < 30; ++i){
			if(i < 7){
				if(cart_day_flag[i])
					cart_days[0]++;
			}
			if(i < 15){
				if(cart_day_flag[i])
					cart_days[1]++;
			}
			if(cart_day_flag[i])
				cart_days[2]++;
		}
		
		result.set(0, key.getString("item_id"));
		result.set(1, buy_cnt);//总销量
		result.set(2, cart_cnt);//加入购物车总量
		result.set(3, buy_user_cnt);//购买的用户数
		result.set(4, cart_user_cnt);//加入购物车用户数
		if(contact_cnt != 0)
			result.set(5, 1.0 * buy_cnt / contact_cnt);//品牌转化率
		else {
			result.set(5, 1.0);
		}
		if(buy_user_cnt != 0){
			result.set(6, 1.0 * buy_cnt / buy_user_cnt);//人均销量
			result.set(8, 1.0 * back_user_cnt / buy_user_cnt);//回头客比率
		}
		else{
			result.set(6, 0.0);//人均销量
			result.set(8, 0.0);//回头客比率
		}
		if(contact_user_cnt != 0)
			result.set(7, 1.0 * buy_user_cnt / contact_user_cnt);
		else 
			result.set(7, 1.0);
		if(cart_user_cnt != 0){
			result.set(9, 1.0 * cart_cnt / cart_user_cnt);//人均加入购物车数量
//			result.set(11, 1.0 * back_user_cart_cnt / cart_user_cnt);//加入购物车回头客比率
		}
		else{
			result.set(9, 0.0);//人均加入购物车数量
//			result.set(11, 0.0);//加入购物车回头客比率
		}
		if(contact_user_cnt != 0)
			result.set(10, 1.0 * cart_user_cnt / contact_user_cnt);
		else 
			result.set(10, 1.0);
		result.set(11, back_user_cnt);//回头客数量
		result.set(12, back_user_cart_cnt);//加入购物车回头客数量
		for(int i = 0; i < 5; ++i)
			result.set(13 + i, final_item_beh_hour[i]);//品牌最近被交互的时间
		for(int i = 0; i < 5; ++i){
			result.set(18 + i, cart_users[i]);
			result.set(23 + i, buy_users[i]);
			result.set(28 + i, beh_users[i]);
		}
		for(int i = 0; i < 3; ++i){
			result.set(33 + i, cart_days[i]);
			result.set(36 + i, buy_days[i]);
			result.set(39 + i, beh_days[i]);
		}
		context.write(result);
	}

	public static long getHourSpan(String sj1, String sj2) {
		SimpleDateFormat myFormatter = new SimpleDateFormat("yyyy-MM-dd HH");
		long day = 0;
		try {
			Date date1 = myFormatter.parse(sj1);
			Date date2 = myFormatter.parse(sj2);
			day = (date1.getTime() - date2.getTime()) / (60 * 60 * 1000);
		} catch (Exception e) {
			return -1;
		}
		return day;
	}

	public void cleanup(TaskContext arg0) throws IOException {

	}
}
