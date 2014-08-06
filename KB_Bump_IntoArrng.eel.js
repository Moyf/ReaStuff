////////////////////////////////////////////////////////////////
function KB_Bump_IntoArrng(cmd)(
////////////////////////////////////////////////////////////////
	
	match("*|w_data|*", cmd) == 1 ? w_data = 1;
	match("*|move|*", cmd) == 1 ? move = 1;
	counter		= 0;
	arrng_nm	="A R R A N G E M E N T";
		
	
	
	move ? Main_OnCommand(NamedCommandLookup("_S&M_CUTSNDRCV1"), 0) // Cut selected tracks (with routing)	
	: (
		Main_OnCommand(NamedCommandLookup("_S&M_COPYSNDRCV1") , 0); // Copy selected tracks (with routing)		
		w_data ? Main_OnCommand(NamedCommandLookup("_SWS_DELALLITEMS") , 0); //  Delete all items on selected track
	);
		
	
	!( arrng_id = KB_Track_Op(arrng_nm,"|sel|exact|exclusive|") ) ? ( msg("Couldnt find the track: "); msg(arrng_nm); );
	
	0;
	msg("Got here");
	
	arrng_idx			=GetMediaTrackInfo_Value(arrng_id, "IP_TRACKNUMBER");
	arrng_folder_d		=GetMediaTrackInfo_Value(arrng_id, "I_FOLDERDEPTH");


	i=0; break=0; 
	while(arrng_folder_d == 1 && !break) ? (
		C_track		=GetTrack(0, (arrng_idx+i)-1);
		C_depth		=GetMediaTrackInfo_Value(C_track, "I_FOLDERDEPTH");
		N_track		=GetTrack(0, (arrng_idx+i));
		N_depth		=GetMediaTrackInfo_Value(N_track, "I_FOLDERDEPTH");
		
		// msg("(begin) C_depth: " + str(C_depth) + ", counter: " + str(counter) + "\n")
		
		C_depth == 1 ? counter += 1:(
			C_depth == -1 ? (
				counter -= 1;
				// msg("C_depth: " + str(C_depth) + ", -counter: " + str(counter) + "\n")
				
				!counter ? (
					SetMediaTrackInfo_Value(arrng_id, "I_SELECTED", 0);
					SetMediaTrackInfo_Value(C_track, "I_SELECTED", 1);
					// msg("got here. counter: " + str(counter) + "\n")
					// return
					
					Main_OnCommand(NamedCommandLookup("_S&M_PASTSNDRCV1") , 0); // Paste tracks (with routing) or items		
					
					SetMediaTrackInfo_Value(C_track, "I_FOLDERDEPTH", 0);
					
					SetMediaTrackInfo_Value(GetSelectedTrack(0,CountSelectedTracks(0)-1), "I_FOLDERDEPTH", -1);
					break=1;
				);
			);
		);
		i += 1
	);
	
	arrng_folder_d != 1 ? (
		Main_OnCommand(NamedCommandLookup("_S&M_PASTSNDRCV1") , 0);
		SetMediaTrackInfo_Value(arrng_id, "I_SELECTED", 1);
		Main_OnCommand(NamedCommandLookup("_SWS_MAKEFOLDER") , 0) ;// Make folder from selected tracks
	);
		
	SetMediaTrackInfo_Value(arrng_id, "I_SELECTED", 0);
	Main_OnCommand(40913, 0); // Vertical scroll selected tracks into view
	SetMediaTrackInfo_Value(arrng_id, "I_FOLDERCOMPACT", 0);			//unfold selected track
	KB_UpdateView();
	
	
	// if arrng_folder_d != 1:
		// SetMediaTrackInfo_Value(arrng_id, "I_FOLDERDEPTH", 1)
	// return
	
	// Main_OnCommand(40001 , 0) // Insert New Track
	
	// return



);
