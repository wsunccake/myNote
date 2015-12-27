# LOG4J

![LOG4J_logo](http://logging.apache.org/log4j/2.x/images/logo.jpg)

Log4j 是一套開放源碼的工具, 方便編程人員在程式中加入 log 機制, 並輸出到各種目標上. Log4j 能夠透過外部的設定檔 (properites 或 XML) 進行設定. Log4j 能夠將 log message 寫到 console, file, stream, TCP, Unix Syslog daemon 等. Log4j 具有 5 種 log 層級 (DEBUG, INFO, WARN, ERROR, FATAL), 可用於不同的系統狀態下所產生的訊息.

Log4j 三大元件:

`Logger` - 由編程人員在程式中使用,進行 logging 的元件

`Appender` - 負責將 log message 輸出到各種裝置上

`Layout` - 決定 log message 的格式

Log4j 的階層架構 :

一個程式中可以擁有多個 Logger,這些 Logger之間以名稱區分,並以此區分出階層. 例如有一個 Logger 的名稱為 "com.foo", 那麼另一個名為 "com.foo.bar" 的 Logger 就隸屬於 "com.foo" logger, 如果 "com.foo.bar" 未定義自己的 log 等級,則以 "com.foo" 的 log 等級為預設值.

階層的最高為 root logger. Root logger 一定在存, 不具有名稱屬性, 可以隨時在程式中以 Logger.getRootLogger() 取得, 其它 logger 則以 Logger.getLogger(String loggerName) 取得.

`Logger`

Logger 可以被指派等級. 能夠指派給 Logger 的等級有: DEBUG, INFO, WARN, ERROR, FATAL 5 種, 定義在 org.apache.log4j.Level 類別中. 這 5 種等級的高低順序為 FATAL > ERROR > WARN > INFO > DEBUG.

Logger 的等級決定它產生 log message 的數量: Logger 只寫 "出高於或等於本身等級" 的 log message. 例如某個 Logger 的等級被設定為 WARN, 那麼它只會寫出等級為 WARN, ERROR, FATAL 的 log message, 對於 DEBUG, INFO 的 log message 則不予理會.

若是 Logger 的等級未被設定, 則會自動使用 parent (上一層) 的等級. 如果程式中所有的 Logger 都未設定等級, 則由 root logger 決定.

Logger 之間以名稱區分, 所以在程式中任何地方, 呼叫 Logger.getLogger(), 並傳入同一個 Logger 名稱, 則會得到同一個 Logger 的 reference.

Logger 之間以名稱區分出階層. 即使父階層在程式中出現的時機比子階層晚, 例如 "com.foo" logger 比 "com.foo.bar" 被取得的時間來得晚, "com.foo" 仍然是 "com.foo.bar" 的父階層 (會影響到子階層 logger 未被定義的屬性, log 等級, appender, layout).

`Appender`

透過 Appender, Logger 能夠將 log message 輸出到指定的裝置上。一個 Logger 能夠擁有多個 Appender,所以 Logger 能夠同時將 log message 輸出到多個個裝置上.

Appender 的設定亦會反映在 Logger 的階層中. 當 Logger 輸出一筆 log message 時, 父階層的 Appender 和自己的 Appender (如果有的話) 都會記錄到這筆 log message; 例如 "com.foo" Logger 有一個 Appender 將 log message 輸出到 console, 而 "com.foo.bar" 有一個 Appender 將 log message 輸出到檔案; 當 "com.foo.bar" Logger 輸出一筆 log message 時, console 和檔案都會出現這筆 log message. 而最簡單的例子, 就是當 root logger 擁有一個輸出到 console 的 Appender 時, 則程式中所有的 logger 所產生的 log message 都會輸出到 console. 唯一個例外的情況, 就是當某個 logger 將自己的 additivity 屬性設為 false (Logger.setAdditivity(false)), 則此 logger 與隸屬於它的子 logger 都不會將 log message 寫到 console.

`Layout`

編程人員透過 Layout 的配置, 能夠自由改變 Logger 寫出 log message 的格式. 例如, 為 Logger 加入一個 conversion pattern 為 "%r [%t] %-5p %c - %m%n" 的 PatternLayout, 則輸出的 log message 就可能會像下列這樣:

	176 [main] INFO  org.foo.Bar - Located nearest gas station.

PatternLayout 格式字元列表如下:

%c 輸出日誌訊息所屬的類別的全名

%d 輸出日誌時間點的日期或時間, 指定格式的方式: %d{yyy-MM-dd HH:mm:ss }

%l 輸出日誌事件的發生位置, 即輸出日誌訊息的語句處於它所在的類別的第幾行

%m 輸出代碼中指定的訊息, 如 log (message) 中的 message

%n 輸出一個列尾符號

%p 輸出優先階層, 即 DEBUG, INFO, WARN, ERROR, FATAL. 如果是調用 debug() 輸出的, 則為 DEBUG, 依此類推. -5p 代表將此字串填滿至 5 個字元, 以空白補不足處

%r 輸出自應用啟動到輸出該日誌訊息所耗費的毫秒數

%t 輸出產生該日誌事件的線程名

%f 輸出日誌訊息所屬的類別的類別名

Layout 亦會反映在 Logger 的階層上


## Example

下載

	rhel:~ # wget ftp://ftp.twaren.net/Unix/Web/apache/logging/log4j/1.2.17/log4j-1.2.17.tar.gz
	rhel:~ # tar zxf log4j-1.2.17.tar.gz


範例

	rhel:~ # cat HelloExample.java
	import org.apache.log4j.Logger;
	
	public class HelloExample{
	    final static Logger logger = Logger.getLogger(HelloExample.class);

	    public static void main(String[] args) {
	        HelloExample obj = new HelloExample();
	        obj.runMe("Hell LOG4J");
	    }

		private void runMe(String parameter){
	        if (logger.isDebugEnabled())
	            logger.debug("This is debug : " + parameter);

	        if (logger.isInfoEnabled())
	            logger.info("This is info : " + parameter);

	        logger.warn("This is warn : " + parameter);
	        logger.error("This is error : " + parameter);
	        logger.fatal("This is fatal : " + parameter);
	    }
	}


Log4j 設定檔

	rhel:~ # cat log4j.properties
	# Define the root logger with appender file
	log = /root/log4j
	log4j.rootLogger = DEBUG, FILE

	# Define the file appender
	log4j.appender.FILE=org.apache.log4j.FileAppender
	log4j.appender.FILE.File=${log}/log.out

	# Define the layout for file appender
	log4j.appender.FILE.layout=org.apache.log4j.PatternLayout
	log4j.appender.FILE.layout.conversionPattern=%m%n


編譯與執行

	rhel:~ # java -cp apache-log4j-1.2.17/log4j-1.2.17.jar HelloExample.java
	rhel:~ # java -cp apache-log4j-1.2.17/log4j-1.2.17.jar -Dlog4j.configuration=file:///root/log4j.properties HelloExample


## Log 輸出到 console

	import org.apache.log4j.*;

	public class DemoLog4J {
	    public static Logger logger = Logger.getLogger(DemoLog4J.class);
	    public static void main(String[] args) {
	        String pattern = "Milliseconds since program start: %r %n" +
	                "Classname of caller: %C %n" +
	                "Date in ISO8601 format: %d{ISO8601} %n" +
	                "Location of log event: %l %n" +
	                "Message: %m %n %n";

	        PatternLayout layout = new PatternLayout(pattern);
	        ConsoleAppender appender = new ConsoleAppender(layout);
	
	        logger.addAppender(appender);
	        logger.setLevel((Level) Level.DEBUG);
	
	        logger.debug("Here is some DEBUG");
	        logger.info("Here is some INFO");
	        logger.warn("Here is some WARN");
	        logger.error("Here is some ERROR");
	        logger.fatal("Here is some FATAL");
	    }
	}


# commons loggin + LOG4J

![commons logging](https://commons.apache.org/logging/)

原始碼

	rhel:~ # cat mypackage/DemoLog.java 
	package mypackage;

	import org.apache.commons.logging.Log;
	import org.apache.commons.logging.LogFactory;
	
	public class DemoLog{
	    static Log logger = LogFactory.getLog(DemoLog.class);

	    public static void main(String[] args) {
	        logger.debug("Here is some DEBUG");
	        logger.info("Here is some INFO");
	        logger.warn("Here is some WARN");
	        logger.error("Here is some ERROR");
	        logger.fatal("Here is some FATAL");
	    }
	}

設定檔

	rhel:~ # cat log4j.properties 
	# Define the root logger with appender file
	log = /root/log4j
	log4j.rootLogger = DEBUG, FILE

	# Define the file appender
	log4j.appender.FILE=org.apache.log4j.FileAppender
	log4j.appender.FILE.File=${log}/log.out

	# Define the layout for file appender
	log4j.appender.FILE.layout=org.apache.log4j.PatternLayout
	log4j.appender.FILE.layout.conversionPattern

編譯執行

	rhel:~ # javac -cp commons-logging-1.2.jar:log4j-1.2.17.jar mypackage/DemoLog.java
	rhel:~ # jar cf mypackage.jar mypackage
	rhel:~ # java -cp commons-logging-1.2.jar:log4j-1.2.17.jar:mypackage.jar -Dlog4j.configuration=file:///root/log4j.properties mypackage.DemoLog
	rhel:~ # ls log4j/log.out