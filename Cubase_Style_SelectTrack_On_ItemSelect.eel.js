function SelectTrack_OnItemSelect_Monitor() local(stored_total)(
	stored=1;
	stored_t=3333;
	
	// Clear old items.
	(stored_total > 0) ? (
		i=0;
		loop(stored_total,
			re_do=0;
			has_selected=0;
			new_stored=0;
			deleted=0;
			
			selected=IsMediaItemSelected(stored[i]);
			!(t = GetMediaItem_Track(stored[i])) ? deleted = 1;
			
			t != stored_t[i] ? (
				new_stored=t;
			);
			
			//Deselect the track if it moved or it no longer has selected items and there's >=1 other track(s) selected.
			IsTrackSelected(stored_t[i]) && (new_stored || (!selected && stored_total > 1) ) ?(
				t_items=CountTrackMediaItems(stored_t[i]) > 0 ? (
					k=0;
					sel_count=CountSelectedMediaItems(0);
					while (k<=sel_count && !has_selected)(
						si=GetSelectedMediaItem(0, k);
						stored[i]!=si ? stored_t[i]==GetMediaItem_Track(si) ? has_selected=1;
						k+=1;
					);		
				);
				
				!has_selected ? (SetMediaTrackInfo_Value(stored_t[i], "I_SELECTED", 0); );
			);
				
			(new_stored) ? (
				stored_t[i]=t;
				SetMediaTrackInfo_Value(stored_t[i], "I_SELECTED", 1); 
			);
			
			!selected ? (
				stored_total == 1 ? (stored[i]=0; stored_t[i]=0;) : (
					// Inline the list.
					stored[i] = stored[stored_total-1]; 
					stored_t[i] = stored_t[stored_total-1]; 
					
					stored[stored_total-1] = 0; 
					stored_t[stored_total-1] = 0; 
					
					re_do=1; 
				);
				stored_total-=1;
			);
		!re_do ? i += 1
		);
	);
	
	// Find and evaluate new items.
	((items = CountSelectedMediaItems(0)) == 0) ? (
		memset(stored,0,1024);
		memset(stored_t,0,1024);
		stored_total=0;
	)
	:(
		i=0; 
		loop(items,
			
			sel_item = GetSelectedMediaItem(0, i);
			found=0;
			
			// Check for old item
			(stored_total > 0) ? (
				j=0; 
				while (j<=stored_total and !found)(
					sel_item == stored[j] ? found=1;	
					j+=1
				);
			);
			
			// Found new item
			(found == 0) ? (
				stored[stored_total]=sel_item;
				stored_t[stored_total]=GetMediaItem_Track(sel_item);
				
					stored_total+1 > 1 ? SetMediaTrackInfo_Value(stored_t[stored_total], "I_SELECTED", 1) :(
					SetOnlyTrackSelected(stored_t[stored_total]);
					);
				stored_total+=1;
			);
			
			i+=1;
		);
		
	);
	defer("SelectTrack_OnItemSelect_Monitor();")
);

SelectTrack_OnItemSelect_Monitor();
