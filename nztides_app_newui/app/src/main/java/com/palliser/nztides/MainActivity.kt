package com.palliser.nztides

import android.content.res.AssetManager
import android.os.Bundle
import android.view.Menu
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.rememberScrollableState
import androidx.compose.foundation.gestures.scrollable
import androidx.compose.foundation.gestures.snapping.rememberSnapFlingBehavior
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.palliser.nztides.ui.theme.NZTidesTheme
import java.io.DataInputStream
import java.io.IOException
import java.text.DecimalFormat
import java.text.SimpleDateFormat
import java.util.Date

class MainActivity : ComponentActivity() {

    //static
    val MENU_ITEM_CHOOSE_PORT: Int = Menu.FIRST

    //static
    val MENU_ITEM_ABOUT: Int = Menu.FIRST + 1

    //static
    val PREFS_NAME: String = "NZTidesPrefsFile" //file to store prefs


    //@Composable
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()


        setContent {
            NZTidesTheme {
                Scaffold { innerPadding ->
                    val scrollState = rememberScrollState()
                    //MinimalDropdownMenu()
                    Text(
                        calc_outstring(currentport),
                        modifier = Modifier
                            .padding(innerPadding)
                            .verticalScroll(scrollState),
                        fontFamily = FontFamily.Monospace
                    )


                }
            }
        }
    }

    //override fun onCreateOptionsMenu(menu){
    //
    // }


    val currentport: String = "Auckland"

    val portdisplaynames = arrayOf(
        "Akaroa",
        "Anakakata Bay",
        "Anawhata",
        "Auckland",
        "Ben Gunn Wharf",
        "Bluff",
        "Castlepoint",
        "Charleston",
        "Dargaville",
        "Deep Cove",
        "Dog Island",
        "Dunedin",
        "Elaine Bay",
        "Elie Bay",
        "Fishing Rock - Raoul Island",
        "Flour Cask Bay",
        "Fresh Water Basin",
        "Gisborne",
        "Green Island",
        "Halfmoon Bay - Oban",
        "Havelock",
        "Helensville",
        "Huruhi Harbour",
        "Jackson Bay",
        "Kaikōura",
        "Kaingaroa - Chatham Island",
        "Kaiteriteri",
        "Kaituna River Entrance",
        "Kawhia",
        "Korotiti Bay",
        "Leigh",
        "Long Island",
        "Lottin Point - Wakatiri",
        "Lyttelton",
        "Mana Marina",
        "Man o'War Bay",
        "Manu Bay",
        "Māpua",
        "Marsden Point",
        "Matiatia Bay",
        "Motuara Island",
        "Moturiki Island",
        "Napier",
        "Nelson",
        "New Brighton Pier",
        "North Cape - Otou",
        "Oamaru",
        "Ōkukari Bay",
        "Omaha Bridge",
        "Ōmokoroa",
        "Onehunga",
        "Opononi",
        "Ōpōtiki Wharf",
        "Opua",
        "Owenga - Chatham Island",
        "Paratutae Island",
        "Picton",
        "Port Chalmers",
        "Port Ōhope Wharf",
        "Port Taranaki",
        "Pouto Point",
        "Raglan",
        "Rangatira Point",
        "Rangitaiki River Entrance",
        "Richmond Bay",
        "Riverton - Aparima",
        "Scott Base",
        "Spit Wharf",
        "Sumner Head",
        "Tamaki River",
        "Tarakohe",
        "Tauranga",
        "Te Weka Bay",
        "Thames",
        "Timaru",
        "Town Basin",
        "Waihopai River Entrance",
        "Waitangi - Chatham Island",
        "Weiti River Entrance",
        "Welcombe Bay",
        "Wellington",
        "Westport",
        "Whakatāne",
        "Whanganui River Entrance",
        "Whangārei",
        "Whangaroa",
        "Whitianga",
        "Wilson Bay"
    )

    fun swap(value: Int): Int {
        val b1 = (value shr 0) and 0xff
        val b2 = (value shr 8) and 0xff
        val b3 = (value shr 16) and 0xff
        val b4 = (value shr 24) and 0xff

        return (b1 shl 24) or (b2 shl 16) or (b3 shl 8) or (b4 shl 0)
    }

    fun calc_outstring(port: String): String {

        val am = getAssets();
        val outstring = StringBuilder()

        val num_rows = 8;
        val num_cols = 34;
        var t = 0
        var told: Int;
        var h: Float = 0.0F;
        var hold: Float
        val now = Date();
        val nowsecs = (now.getTime() / 1000).toInt();
        val lasttide: Int
        val graph: Array<Array<Char>> = Array(num_rows) { Array(num_cols + 1) { ' ' } }
        //char [][] graph = new char[num_rows][num_cols+1];


        var stringBuilder = try {

            val nformat1 = DecimalFormat(" 0.00;-0.00")
            val nformat2 = DecimalFormat("0.00")
            val nformat3 = DecimalFormat("00")
            val nformat4 = DecimalFormat(" 0.0;-0.0")

            //SimpleDateFormat dformat = new SimpleDateFormat(
            //    	"HH:mm E dd-MM-yyyy zzz");
            val dformat = SimpleDateFormat("HH:mm E dd/MM/yy zzz");

            val tidedat = DataInputStream(am.open(port + ".tdat", 1));


            val stationname_tofu = tidedat.readLine(); //stationname with unicode stuff ups
            // byte[] stationnamebytes = stationname_tofu.getBytes(Charset.defaultCharset());
            //String stationname = new String(stationnamebytes, "UTF-8");
            //read timestamp for last tide in datafile
            val lasttide = swap(tidedat.readInt());

            //nrecs = swap(tidedat.readInt()); //Number of records in datafile
            tidedat.readInt(); //Read number of records in datafile

            told = swap(tidedat.readInt());
            hold = (tidedat.readByte()).toFloat() / 10.0F

            if (told > nowsecs) {
                outstring.append("The first tide in this datafile doesn't occur until ")
                outstring.append(dformat.format(Date(1000 * told.toLong())))
                outstring.append(". The app should start working properly about then.")
            } else {

                //look thru tidedatfile for current time
                while (true) {
                    t = swap(tidedat.readInt());
                    h = (tidedat.readByte()).toFloat() / 10.0F
                    if (t > nowsecs) {
                        break
                    }
                    told = t
                    hold = h
                }


                //parameters of cosine wave used to interpolate between tides
                //We assume that the tides vaires cosinusoidally
                //between the last tide and the next one
                //see NZ Nautical almanac for more details,
                val omega = 2 * Math.PI / ((t - told) * 2);
                val amp = (hold - h) / 2;
                val mn = (h + hold) / 2;
                var x: Double
                var phase: Double

                // make ascii art plot

                for (k in 0 until num_rows) {
                    for (j in 0 until num_cols) {
                        graph[k][j] = ' ';
                    }
                    graph[k][num_cols] = '\n';
                }

                for (k in 0 until num_cols) {
                    x =
                        (1.0 + (if (hold > h) -1 else 1) * Math.sin(k * 2 * Math.PI / (num_cols - 1))) / 2.0
                    x = ((num_rows - 1) * x + 0.5);
                    graph[x.toInt()][k] = '*';
                    //graph[k%num_rows][k]='*';
                }

                phase = omega * (nowsecs - told);
                x = (phase + Math.PI / 2) / (2.0 * Math.PI);
                x = ((num_cols - 1) * x + 0.5);
                for (j in 0 until num_rows) {
                    graph[j][x.toInt()] = '|';
                }


                val currentht = amp * Math.cos(omega * (nowsecs - told)) + mn;
                val riserate = -amp * omega * Math.sin(omega * (nowsecs - told)) * 60 * 60;


                //Start populating outstring
                outstring.append("[" + port + "] " + nformat4.format(currentht) + "m");
                //display up arrow or down arrow depending on weather tide is rising or falling
                if (hold < h)
                    outstring.append(" \u2191");//up arrow
                else
                    outstring.append(" \u2193");//down arrow

                outstring.append(nformat2.format(Math.abs(riserate)) + "m/hr\n");
                outstring.append("---------------\n");

                val time_to_previous = (nowsecs - told);
                val time_to_next = (t - nowsecs);
                var hightidenext = (h > hold);

                if (time_to_previous < time_to_next) {
                    if (hightidenext) {
                        outstring.append(
                            "Low tide (" + hold + "m) " + (time_to_previous / 3600) +
                                    "h" + nformat3.format(((time_to_previous / 60) % 60)) + "m ago\n"
                        )
                    } else {
                        outstring.append(
                            "High tide (" + hold + "m) " + (time_to_previous / 3600) +
                                    "h" + nformat3.format((time_to_previous / 60) % 60) + "m ago\n"
                        );
                    }
                } else {
                    if (hightidenext) {
                        outstring.append(
                            "High tide (" + h + "m) in " + (time_to_next / 3600) +
                                    "h" + nformat3.format((time_to_next / 60) % 60) + "m\n"
                        );
                    } else {
                        outstring.append(
                            "Low tide (" + h + "m) in " + (time_to_next / 3600) +
                                    "h" + nformat3.format((time_to_next / 60) % 60) + "m\n"
                        );
                    }

                }
                //outstring.append("---------------\n");
                //int num_minutes=(int)((nowsecs-told)/(60));
                //outstring.append("Last tide " + hold + "m,    "+num_minutes/60  + "h" +nformat3.format(num_minutes%60) +"m ago\n");
                //num_minutes=(int)((t -nowsecs)/(60));
                //outstring.append("Next tide " + h + "m, in " +num_minutes/60  + "h" +nformat3.format(num_minutes%60) +"m\n");
                //outstring.append("---------------\n");
                outstring.append("\n");

                for (k in 0 until num_rows) {
                    for (j in 0 until (num_cols + 1)) {
                        outstring.append(graph[k][j])
                    }
                }

                //outstring.append("---------------\n");
                outstring.append("\n");


                hightidenext = !hightidenext
                outstring.append(
                    nformat1.format(hold) + (if (hightidenext)
                        " H " else " L ") + dformat.format(Date(1000L * told.toLong())) + '\n'
                )
                hightidenext = !hightidenext
                outstring.append(
                    nformat1.format(h) + (if (hightidenext)
                        " H " else " L ") + dformat.format(Date(1000L * told.toLong())) + '\n'
                )

                for (k in 0 until (35 * 4)) { //about a month of tides
                    hightidenext = !hightidenext;
                    t = swap(tidedat.readInt());
                    h = (tidedat.readByte()).toFloat() / 10.0F;
                    outstring.append(
                        nformat1.format(h) + (if (hightidenext) " H " else " L ") + dformat.format(
                            Date(1000L * t.toLong())
                        ) + '\n'
                    );
                }
                outstring.append("The last tide in this datafile occurs at:\n");
                outstring.append(dformat.format(Date(1000L * lasttide.toLong())));
            }

        } catch (e: IOException) {
            outstring.append("Problem reading tide data\n\n Try selecting the port again, some times the ports available change with and upgrade. If this doesn't work it is either because the tide data is out of date or you've found some bug, try looking for an update.");
        }
        return outstring.toString();
    }

}

    @Composable
    fun MinimalDropdownMenu() {
        var expanded = false
        //  var expanded  by remember { mutableStateOf(false) }
        Box(
            modifier = Modifier.padding(16.dp)
        ) {
            IconButton(onClick = { expanded = !expanded }) {
                Icon(Icons.Default.MoreVert, contentDescription = "More options")
            }
            DropdownMenu(
                expanded = expanded,
                onDismissRequest = { expanded = false }
            ) {
                DropdownMenuItem(
                    text = { Text("Option 1") },
                    onClick = { /* Do something... */ }
                )
                DropdownMenuItem(
                    text = { Text("Option 2") },
                    onClick = { /* Do something... */ }
                )
            }
        }
    }




