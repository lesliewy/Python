db.getCollection("financial_lrb").find({}).count()
db.getCollection("financial_xjllb").find({}).count()
db.getCollection("financial_zcfzb").find({}).count()

db.system.js.save(
   {
     _id : "myAddFunction" ,
     value : function (x, y){ return x + y; }
   }
);
db.loadServerScripts();
myAddFunction(1, 2)

/* 
现金占比: 货币资金/资产总计;
*/
db.financial_zcfzb.aggregate(
	[
		{$match: {code:"002769"}},
		{$project:{"总资产": "$资产.非流动资产.资产总计(万元).20171231", 
		           "货币资金":"$资产.流动资产.货币资金(万元).20171231", 
		           "a": {$toInt: "$资产.流动资产.货币资金(万元).20171231"}
		          // "货币资金/总资产": {$divide: ["$资产.流动资产.货币资金(万元).20171231", "$资产.非流动资产.资产总计(万元).20171231"]}
				  }
		}
	]
)

db.loadServerScripts();
db.financial_zcfzb.aggregate(
	[
		{$match: {code:"000001"}},
		{$project: {"a": myAddFunction(1,2)}
		}
	])
db.getCollection("financial_zcfzb").find({"code":"002769"}, {"资产.非流动资产.资产总计(万元)":1, "资产.流动资产.货币资金(万元)":1, "负债.非流动负债.负债合计(万元)":1});
db.getCollection("financial_zcfzb").find({"code":"600697"});
db.getCollection("financial_xjllb").find({"code":"600697"});
db.getCollection("financial_lrb").find({"code":"600697"});

