package com.palliser.nztides;

import java.io.DataInputStream;
import java.io.IOException;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

import android.app.Activity;
import android.content.SharedPreferences;
import android.content.res.AssetManager;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.SubMenu;
import android.widget.ScrollView;
import android.widget.TextView;

public class NZTides extends Activity {
	
    public static final int MENU_ITEM_CHOOSE_PORT = Menu.FIRST;
    public static final int MENU_ITEM_ABOUT = Menu.FIRST+1;
    public static final String PREFS_NAME = "NZTidesPrefsFile";//file to store prefs

    
   private String currentport;
   
   /* private String[] portlist = {
		   "auckland",
		   "bluff",
		   "dunedin",
		   "gisborne",
		   "lyttelton",
		   "marsden point",
		   "napier",
		   "nelson",
		   "onehunga",
		   "picton",
		   "port chalmers",
		   "port taranaki",
		   "tauranga",
		   "timaru",
		   "wellington",
		   "westport"
   	};
   
   private String[] portdisplaynames = {
		   "Auckland",
		   "Bluff",
		   "Dunedin",
		   "Gisborne",
		   "Lyttelton",
		   "Marsden Point",
		   "Napier",
		   "Nelson",
		   "Onehunga",
		   "Picton",
		   "Port Chalmers",
		   "Port Taranaki",
		   "Tauranga",
		   "Timaru",
		   "Wellington",
		   "Westport"cd
   	};
*/

	private String[] portlist = {"anawhata", "auckland", "ben gunn", "bluff", "castlepoint", "deep cove", "dunedin", "fishing rock", "flour cask bay", "french bay", "fresh water basin", "gisborne", "green island", "havelock", "huruhi harbour", "jackson bay", "kaikoura", "kaingaroa", "kaiteriteri", "kaituna river", "kawhia", "korotiti bay", "leigh", "lottin point", "lyttelton", "mana", "mano war bay", "mapua", "marsden point", "matiatia bay", "napier", "nelson", "north cape", "oamaru", "oban", "omokoroa", "onehunga", "opotiki wharf", "opua", "owenga", "paratutae island", "picton", "port chalmers", "port ohope wharf", "port taranaki", "pouto point", "preservation inlet", "raglan", "rocky point", "scott base", "spit wharf", "sumner", "tarakohe", "tauranga", "timaru", "waiorua bay", "waitangi (chatham is)", "whanganui", "wellington", "westport", "whakatane", "whangarei", "whangaroa", "whitianga"};

    private String[] portdisplaynames = {"Anawhata", "Auckland", "Ben Gunn", "Bluff", "Castlepoint", "Deep Cove", "Dunedin", "Fishing Rock", "Flour Cask Bay", "French Bay", "Fresh Water Basin", "Gisborne", "Green Island", "Havelock", "Huruhi Harbour", "Jackson Bay", "Kaikoura", "Kaingaroa", "Kaiteriteri", "Kaituna River", "Kawhia", "Korotiti Bay", "Leigh", "Lottin Point", "Lyttelton", "Mana", "Man o\'War Bay", "Mapua", "Marsden Point", "Matiatia Bay", "Napier", "Nelson", "North Cape", "Oamaru", "Oban", "Omokoroa", "Onehunga", "Opotiki Wharf", "Opua", "Owenga", "Paratutae Island", "Picton", "Port Chalmers", "Port Ohope Wharf", "Port Taranaki", "Pouto Point", "Preservation Inlet", "Raglan", "Rocky Point", "Scott Base", "Spit Wharf", "Sumner", "Tarakohe", "Tauranga", "Timaru", "Waiorua Bay", "Waitangi (Chatham Is)", "Whanganui", "Wellington", "Westport", "Whakatane", "Whangarei", "Whangaroa", "Whitianga"};

	public static int swap (int value)
	{
	  int b1 = (value >>  0) & 0xff;
	  int b2 = (value >>  8) & 0xff;
	  int b3 = (value >> 16) & 0xff;
	  int b4 = (value >> 24) & 0xff;

	  return b1 << 24 | b2 << 16 | b3 << 8 | b4 << 0;
	}

	public String calc_outstring(String port){
	       
		AssetManager am = getAssets();
		StringBuffer outstring =  new StringBuffer("");
	        
		int num_rows=8;
	    int num_cols=34;
		int t = 0,told;
		float h=0;
		float hold;
		Date now = new Date();
		int nowsecs = (int)(now.getTime()/1000);
		int lasttide;
		char [][] graph = new char[num_rows][num_cols+1];


		
		
	    try {
	    	DataInputStream tidedat = new DataInputStream(am.open(port+".tdat",1));
	    	String stationname = tidedat.readLine();
	        
	    	//read timestamp for last tide in datafile
	    	lasttide = swap(tidedat.readInt());
	    	 
	    	//nrecs = swap(tidedat.readInt()); //Number of records in datafile
	        tidedat.readInt(); //Read number of records in datafile
	       
	    	told=0;
	        hold=0;

	        //look thru tidedatfile for current time
	        for(;;){
	        	t = swap(tidedat.readInt());
	            h = (float) (tidedat.readByte())/(float)(10.0);
	            if(t>nowsecs){
	                break;
	            }
	            told = t;
	            hold = h;
	        }
	        

	        DecimalFormat  nformat1 = new DecimalFormat(" 0.00;-0.00");
	        DecimalFormat  nformat2 = new DecimalFormat("0.00");
	        DecimalFormat  nformat3 = new DecimalFormat("00");
	        DecimalFormat  nformat4 = new DecimalFormat(" 0.0;-0.0");
	        //SimpleDateFormat dformat = new SimpleDateFormat(
	        //    	"HH:mm E dd-MM-yyyy zzz");
	        SimpleDateFormat dformat = new SimpleDateFormat(
	            	"HH:mm E dd/MM/yy zzz");
	        //parameters of cosine wave used to interpolate between tides
	        //We assume that the tides vaires cosinusoidally
	        //between the last tide and the next one
	        //see NZ Nautical almanac for more details,
	        double omega = 2*Math.PI/((t-told)*2); 
	        double amp = (hold - h)/2;
	        double mn = (h+hold)/2;
	        double x,phase;
     
	        // make ascii art plot
	        
			for(int k=0;k<num_rows;k++){
				for(int j=0;j<num_cols;j++){
					graph[k][j]=' ';
				}
				graph[k][num_cols]='\n';
			}
	        
	        for(int k=0;k<num_cols;k++){
	        	x = ( 1.0+(hold>h?-1:1)*Math.sin( k * 2 * Math.PI / (num_cols-1) ) ) / 2.0;
	        	x = ( (num_rows-1) * x + 0.5 );
	        	graph[(int)x][k]='*';
	        	//graph[k%num_rows][k]='*';
		        }	
	        
	        phase = omega*(nowsecs-told);
	        x = (phase+Math.PI/2)/(2.0*Math.PI);
		    x = ( (num_cols-1) * x + 0.5 );
		    for(int j=0;j<num_rows;j++){
		    	graph[j][(int)x]='|';
		    }
	       
	        
	        double currentht = amp*Math.cos(omega*(nowsecs-told))+mn;
	        double riserate =  -amp*omega*Math.sin(omega*(nowsecs-told))*60*60;



	        //Start populating outstring
	        outstring.append(stationname.trim() + " " + nformat4.format(currentht) +"m");
	        //display up arrow or down arrow depending on weather tide is rising or falling
	        if(hold<h)
	            outstring.append(" \u2191");//up arrow
	        else
	            outstring.append(" \u2193");//down arrow
	           
	        outstring.append(nformat2.format(Math.abs(riserate))+ "m/hr\n");
	        outstring.append("---------------\n");
	        
	        int time_to_previous= (nowsecs-told);
	        int time_to_next = (t-nowsecs);
	        boolean hightidenext=(h>hold);
	        
	        if(time_to_previous<time_to_next){
	        	if(hightidenext){
	        		outstring.append("Low tide ("+hold+"m) " + (int)(time_to_previous/3600) +
	        					"h" +  nformat3.format( (int)(time_to_previous/60) % 60) + "m ago\n");
	        	} else {
	        		outstring.append("High tide ("+hold+"m) " + (int)(time_to_previous/3600) +
        					"h" +  nformat3.format( (int)(time_to_previous/60) % 60) + "m ago\n");
	        	}
	        } else {
	        	if(hightidenext){
	        		outstring.append("High tide ("+h+"m) in " + (int)(time_to_next/3600) +
	        					"h" +  nformat3.format( (int)(time_to_next/60) % 60) + "m\n");
	        	} else {
	        		outstring.append("Low tide ("+h+"m) in " + (int)(time_to_next/3600) +
        					"h" +  nformat3.format( (int)(time_to_next/60) % 60) + "m\n");
	        	}
	        	
	        }
	        //outstring.append("---------------\n");
	        //int num_minutes=(int)((nowsecs-told)/(60));
	        //outstring.append("Last tide " + hold + "m,    "+num_minutes/60  + "h" +nformat3.format(num_minutes%60) +"m ago\n");
	        //num_minutes=(int)((t -nowsecs)/(60));
	        //outstring.append("Next tide " + h + "m, in " +num_minutes/60  + "h" +nformat3.format(num_minutes%60) +"m\n"); 
	        //outstring.append("---------------\n");
	        outstring.append("\n");
	        
	    	for(int k=0;k<num_rows;k++){
				for(int j=0;j<num_cols+1;j++){
					outstring.append(graph[k][j]);
				}
			}
	        
	    	//outstring.append("---------------\n");
	    	outstring.append("\n");
		        
	        
	        
	        
	        
	        

       	 	hightidenext = !hightidenext;
       	 	outstring.append(nformat1.format(hold)+(hightidenext?" H ":" L ")+dformat.format( new Date(1000*(long)told))+'\n'); 
       	 	hightidenext = !hightidenext;
	        outstring.append(nformat1.format(h)+(hightidenext?" H ":" L ")+dformat.format(new Date(1000*(long)t))+'\n');
	            
	            for(int k=0;k<35*4;k++){
	            	 hightidenext = !hightidenext;
	            	  t = swap(tidedat.readInt());
	                  h = (float) (tidedat.readByte())/(float)(10.0);
	                  outstring.append(nformat1.format(h)+(hightidenext?" H ":" L ")+dformat.format(new Date(1000*(long)t))+'\n');
	            }
	            outstring.append("The last tide in this datafile occurs at:\n");
	            outstring.append(dformat.format(new Date(1000*(long)lasttide)));
	            
	        }catch (IOException e) {
	        	outstring.append("Problem reading tide data\nThis is probably because tide data is out of date, try looking for an update.");
	        }
	        return outstring.toString();
	}
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //restore current port from settings file
        SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
        currentport = settings.getString("CurrentPort","auckland" );        
        
    //    setContentView(R.layout.main);
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        super.onCreateOptionsMenu(menu);

        // This is our one standard application action -- inserting a
        // new note into the list.
        SubMenu portMenu = menu.addSubMenu(0, MENU_ITEM_CHOOSE_PORT, 0,"Select Port");
        for(int k=0;k<portlist.length;k++)
        	portMenu.add(0,Menu.FIRST+10+k,0,portdisplaynames[k]);
        
        menu.add(0, MENU_ITEM_ABOUT, 0,"About" );
               
        // Generate any additional actions that can be performed on the
        // overall list.  In a normal install, there are no additional
        // actions found here, but this allows other applications to extend
        // our menu with their own actions.        Intent intent = new Intent(null, getIntent().getData());
       // intent.addCategory(Intent.CATEGORY_ALTERNATIVE);
       // menu.addIntentOptions(Menu.CATEGORY_ALTERNATIVE, 0, 0,                new ComponentName(this, NotesList.class), null, intent, 0, null);
        return true;
    }

    public boolean  onOptionsItemSelected  (MenuItem  item){
    	  //AdapterContextMenuInfo info = (AdapterContextMenuInfo) item.getMenuInfo();
    	
    	int id = item.getItemId();
	    
	    if(id>=Menu.FIRST+10 && id<Menu.FIRST+10+portlist.length){
	    	currentport = portlist[id-11];
	    	this.onResume();
	    	return true;
	    }
	        
    	switch (id) {
    	  case MENU_ITEM_ABOUT:
    		TextView tv = new TextView(this);
    		//tv.setTypeface(Typeface.MONOSPACE);
    		tv.setText(R.string.AboutString);//+now.format2445());
    		ScrollView sv = new ScrollView(this);
    		sv.addView(tv);
    		setContentView(sv);   
    	    //quit();
    	    return true;
    	  default:
    	    return super.onOptionsItemSelected(item);
    	  }
    	}
    
    @Override
    protected void onResume(){
        String outstring = calc_outstring(currentport);
        TextView tv = new TextView(this);
        tv.setTypeface(Typeface.MONOSPACE);
        tv.setText(outstring);//+now.format2445());
        ScrollView sv = new ScrollView(this);
        sv.addView(tv);
        setContentView(sv);   
    	super.onResume();
    }

    @Override
    protected void onStop(){
       super.onStop();
    
      // Save user preferences. We need an Editor object to
      // make changes. All objects are from android.context.Context
      SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
      SharedPreferences.Editor editor = settings.edit();
      editor.putString("CurrentPort", currentport);

      // Don't forget to commit your edits!!!
      editor.commit();
    }


}
