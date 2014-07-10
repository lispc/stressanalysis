package Test;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.FileReader;
import java.lang.Thread.State;
import java.util.List;

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import com.mongodb.Mongo;
import com.mongodb.util.JSON;

import weibo4j.Oauth;
import weibo4j.Timeline;
import weibo4j.Users;
import weibo4j.examples.oauth2.Log;
import weibo4j.http.AccessToken;
import weibo4j.model.Paging;
import weibo4j.model.Status;
import weibo4j.model.StatusWapper;
import weibo4j.model.User;
import weibo4j.model.WeiboException;
import weibo4j.org.json.JSONObject;
import weibo4j.util.BareBonesBrowserLaunch;

public class WeiboCrawler {
	public static final String mongodb_host = "166.111.139.96";
	public static final String weibodb_name = "weibo_Test";
	public static final String user_collection = "weibo_user";
	public static final String status_collection = "weibo_status";
	
	//public static String accessToken = "2.004W4pvB06XASOa817122a91cNcCQE";
	public static String accessToken = "2.00r8ggvC06XASOcf51544ebfzpM32C";
	
	public static Mongo mongo;
	public static DB mongoDB;
	public static DBCollection userCollection;
	public static DBCollection statusCollection;
	
	/*微博用户信息抓取入口对象*/
	public static Users um;
	/*用户微博信息抓取入口对象*/
	public static Timeline tm;
	
	public WeiboCrawler(){
		try{
			mongo = new Mongo(mongodb_host);
			mongoDB = mongo.getDB(weibodb_name);
			userCollection = mongoDB.getCollection(user_collection);
			statusCollection = mongoDB.getCollection(status_collection);
			
			//获取accessToken
//			Oauth oauth = new Oauth();
//			String oauthUrl = oauth.authorize("code", "");
//			BareBonesBrowserLaunch.openURL(oauthUrl);
			
			um = new Users();
			um.client.setToken(accessToken);
			tm = new Timeline();
			tm.client.setToken(accessToken);
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	/*微博OAuth 2.0登录认证获取AccessToken，当AccessToken过期时需要重新运行此函数更新AccessToken*/
	public static void OAuth() {
		try {
			Oauth oauth = new Oauth();
			String oauthUrl = oauth.authorize("code", "");

			BareBonesBrowserLaunch.openURL(oauthUrl);

			System.out.println("oauthUrl = " + oauthUrl);
			System.out.print("Hit enter when it's done.[Enter]:");
			BufferedReader br = new BufferedReader(new InputStreamReader(
					System.in));
			String code = br.readLine();
			Log.logInfo("code: " + code);
			//code = "a759bb5f3f4c687559151f41f63404b0";
			System.out.println(oauth.getAccessTokenByCode(code));
		} catch (WeiboException e) {
			if (401 == e.getStatusCode()) {
				Log.logInfo("Unable to get the access token.");
			} else {
				e.printStackTrace();
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
		
	//public static void CrawUserByUids(String uidListFile, String logFile, String resultUidListFile)
	public static void CrawUserByUids(String uid, String logFile, String resultUidListFile){
//		try
//		{
//			BufferedReader br = new BufferedReader(new FileReader(new File(uidListFile)));
//			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(logFile)));
//			BufferedWriter userWriter = new BufferedWriter(new FileWriter(new File(resultUidListFile)));
//			bw.write("uid\terrorCode");
//			bw.newLine();
//			
//			userWriter.write("uid\ttotalStatusNum");
//			userWriter.newLine();
//			String uid = "";
//			int index = 0;
//			while((uid = br.readLine()) != null)
//			{
//				System.out.println("Crawling index=" + index + " , uid=" + uid + "...");
//				User user = null;
//				try{
//					user = um.showUserById(uid);
//					//user=um.showUserById("2684689767");
//					//System.out.print(user.toString());
//				}catch(WeiboException e)
//				{
//					e.printStackTrace();
//					int errorCode = e.getErrorCode();
//					bw.append(uid + "\t" + errorCode);
//					bw.newLine();
//				}
//				Log.logInfo(user.toString());
//				System.out.println(user.toString());
//				if(user != null)
//				{
//					JSONObject userJSON = user.originJSON;
//					System.out.println("userJSON:" + userJSON.toString());
//					
//					DBObject userObj = (BasicDBObject)JSON.parse(userJSON.toString());
//					userCollection.save(userObj);
//					 
//					int totalStatusNum = user.getStatusesCount();
//					userWriter.append(uid + "\t" + totalStatusNum);
//					userWriter.newLine();
//					index ++;
//				}
//			}
//			
//			bw.close();
//			br.close();
//			userWriter.close();
//			
//			System.out.println("All user info crawled, total num is:" + index + ", start to crawl statuses...");
//			br = new BufferedReader(new FileReader(new File(resultUidListFile)));
//			br.readLine();
//			String line = "";
//			int totalNum = 0;
//			while((line = br.readLine()) != null)
//			{
//				System.out.println("Crawling status index from:" + totalNum);
//				if(line == "") break;
//				String words[] = line.split("\t");
//				if(words.length < 2) break;
//				String curUid = words[0];
//				int curNum = Integer.parseInt(words[1]);
//				CrawlStatusesByUid(curUid, curNum);
//				totalNum += curNum;			
//			}
//			System.out.println("All statuses crawled...total num is:");
//			
//			
//		}catch(Exception e)
//		{
//			e.printStackTrace();
//		}
		
		//uid string
		
		try
		{
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File(logFile)));
			BufferedWriter userWriter = new BufferedWriter(new FileWriter(new File(resultUidListFile)));
			bw.write("uid\terrorCode");
			bw.newLine();
			
			userWriter.write("uid\ttotalStatusNum");
			userWriter.newLine();
			User user = null;
			try{
				user = um.showUserById(uid);
			}catch(WeiboException e)
			{
				e.printStackTrace();
				int errorCode = e.getErrorCode();
				bw.append(uid + "\t" + errorCode);
				bw.newLine();
			}
			Log.logInfo(user.toString());
			//System.out.println(user.toString());
			if(user != null)
			{
				JSONObject userJSON = user.originJSON;
				System.out.println("userJSON:" + userJSON.toString());
					
				DBObject userObj = (BasicDBObject)JSON.parse(userJSON.toString());
				userCollection.save(userObj);
					 
				int totalStatusNum = user.getStatusesCount();
				userWriter.append(uid + "\t" + totalStatusNum);
				userWriter.newLine();
			}
			
			bw.close();
			userWriter.close();
			
			System.out.println("start to crawl statuses...");
			BufferedReader br = new BufferedReader(new FileReader(new File(resultUidListFile)));
			br.readLine();
			String line = "";
			int totalNum = 0;
			while((line = br.readLine()) != null)
			{
				System.out.println("Crawling status index from:" + totalNum);
				if(line == "") break;
				String words[] = line.split("\t");
				if(words.length < 2) break;
				String curUid = words[0];
				int curNum = Integer.parseInt(words[1]);
				CrawlStatusesByUid(curUid, curNum);
				totalNum += curNum;			
			}
			System.out.println("All statuses crawled...total num is:");
			
			
		}catch(Exception e)
		{
			e.printStackTrace();
		}
		
	}
	
	public static void CrawlStatusesByUid(final String uid, final int totalStatusNum)
	{
//		Thread crawlThread = new Thread(){
//			public void run()
//			{
//				try {
//					int countPerPage = 100;
//					int totalPage = totalStatusNum / countPerPage;
//					if(totalStatusNum % countPerPage > 0) totalPage ++;
//					
//					for(int pageIndex = 1; pageIndex < totalPage; pageIndex ++)
//					{
//						Paging page = new Paging(pageIndex, countPerPage);
//						StatusWapper statusWapper = tm.getUserTimelineByUid(uid, page, 0, 0);
//						System.out.println("page index=" + pageIndex + "status num:" + statusWapper.getStatuses().size());
//						List<Status> statuses = statusWapper.getStatuses();
//						for(int i = 0; i < statuses.size(); i ++){
//							Status status = statuses.get(i);
//							DBObject object = (BasicDBObject)JSON.parse(status.originJSON.toString());
//							statusCollection.save(object);
//							System.out.println("pageIndex=" + pageIndex + ", statusIndex=" + i + ", status=" + status);
//							System.err.println(status);
//						}
//						System.out.println("total Num:" + statusWapper.getTotalNumber());
//					}
//				} catch (WeiboException e) {
//					e.printStackTrace();
//				}
//			}
//		};
//		crawlThread.start();
//		State threadState = crawlThread.getState();
//		while(java.lang.Thread.State.TERMINATED != crawlThread.getState())
//		{
//			try {
//				Thread.sleep(5000);
//			} catch (InterruptedException e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
//		}
		
		try {
		int countPerPage = 100;
		int totalPage = totalStatusNum / countPerPage;
		if(totalStatusNum % countPerPage > 0) totalPage ++;
		
		for(int pageIndex = 1; pageIndex < totalPage; pageIndex ++)
		{
			Paging page = new Paging(pageIndex, countPerPage);
			StatusWapper statusWapper = tm.getUserTimelineByUid(uid, page, 0, 0);
			System.out.println("page index=" + pageIndex + "status num:" + statusWapper.getStatuses().size());
			List<Status> statuses = statusWapper.getStatuses();
			for(int i = 0; i < statuses.size(); i ++){
				Status status = statuses.get(i);
				DBObject object = (BasicDBObject)JSON.parse(status.originJSON.toString());
				statusCollection.save(object);
				System.out.println("pageIndex=" + pageIndex + ", statusIndex=" + i + ", status=" + status);
				System.err.println(status);
			}
			System.out.println("total Num:" + statusWapper.getTotalNumber());
		}
	} catch (WeiboException e) {
		e.printStackTrace();
	}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		new WeiboCrawler();
		// TODO Auto-generated method stub
		//WeiboCrawler.OAuth();
		//WeiboCrawler.CrawUserByUids("uids.txt", "uids_exception.txt", "uid_correct.txt");
		WeiboCrawler.CrawUserByUids(args[0], "uids_exception.txt", "uid_correct.txt");

	}

}