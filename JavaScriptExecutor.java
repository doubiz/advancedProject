import javax.script.Compilable;
import javax.script.CompiledScript;
import javax.script.Invocable;
import javax.script.ScriptContext;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import javax.script.SimpleScriptContext;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;

public class JavaScriptExecutor {
	public static void main(String [] args) {
		try {
		ScriptEngineManager factory = new ScriptEngineManager();
	    ScriptEngine engine = factory.getEngineByName("JavaScript");
	    File file = new File(args[0]);
	    FileInputStream fis = new FileInputStream(file);
	    byte[] data = new byte[(int)file.length()];
	    fis.read(data);
	    fis.close();
	    //
	    String s = new String(data, "UTF-8");
	    String script = s;
	    //System.out.println("fun: "+ script);
	    file = new File(args[1]);
	    FileOutputStream fos = new FileOutputStream(file);
	    fos.write(engine.eval(script).toString().getBytes());
	    fos.flush();
	    fos.close();
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}