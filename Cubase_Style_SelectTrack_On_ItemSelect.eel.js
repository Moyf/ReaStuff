


//This EEL script will run in the background: Upon selecting an item, it will select the track it's on.
//Upon deselecting an item, it will deselect the track it's on, if it contains no other selected items.

//I made this  because I preferred the handing of item/track selection in Cubase/Pro Tools. 
//If you're going to use this, make sure you have 'Editing Behaviour > Mouse click/edit in track view changes track selection' unchecked




function i2s(i)(sprintf(#s,"%i",i); #s;);
function msg(s)(ShowConsoleMsg(s));


function SelectTrack_OnItemSelect_Monitor()(
	stored=1;
	
	// CLEAR OLD ITEMS	
	(stored_total > 0) ? (
		i=0;
		
		loop(stored_total,
			re_do=0;
			has_selected=false;
			
			!IsMediaItemSelected(stored[i]) ? (
				
				t = GetMediaItem_Track(stored[i]);
				
				t_items=CountTrackMediaItems(t) > 0 ?(
					k=0;
					loop(CountSelectedMediaItems(0), 
						si=GetSelectedMediaItem(0, k);
						stored[i]!=si ? t==GetMediaItem_Track(si) ? has_selected=true;
						k+=1;
						);		
				);
				
				!has_selected ? (
					SetMediaTrackInfo_Value(t, "I_SELECTED", 0); 
					UpdateArrange();
				);
				
				stored_total == 1 ? stored[i]=0 : (
					// Inline the list.
					stored[i] = stored[stored_total-1]; 
					stored[stored_total-1] = 0; 
					// Don't increment so we can evaluate the moved item.
					re_do=1; 
				);
				
				stored_total-=1;
			);	
		!re_do ? i += 1
		);
	);
	
	((items = CountSelectedMediaItems(0)) == 0) ? (
		memset(stored,0,1024);
		stored_total=0;
	)
	:(
		i=0; 
		loop(items,
			
			sel_item = GetSelectedMediaItem(0, i);
			found=0;
			
			// OLD ITEM
			(stored_total > 0) ? (
				j=0; loop(stored_total,
					sel_item == stored[j] ? found=1;;	
					j+=1
				);
			);
			
			// NEW ITEM
			(found == 0) ? (
				stored[stored_total]=sel_item;
				
				stored_total+=1;
				
				
				(track_id = GetMediaItem_Track(sel_item)) ? (
					stored_total > 1 ? SetMediaTrackInfo_Value(track_id, "I_SELECTED", 1) : SetOnlyTrackSelected(track_id);
					UpdateArrange();
				);
			);
			
			i+=1;
		);
		
	);
	defer("SelectTrack_OnItemSelect_Monitor();")
);

SelectTrack_OnItemSelect_Monitor();
