# ========================================================================#
class TD:
# ========================================================================#
	def __init__(self, id, cmd='all', i=0):
	# ========================================================================#
		
		self.id		= id
		self.idx	= int(RPR_GetMediaTrackInfo_Value(id, "IP_TRACKNUMBER")-1)
		self.i		= i
		
		all			= 'all' in cmd
		if not all: cmd	= cmd.split('|')
		name 		= 'name' in cmd or all
		folder 		= 'folder' in cmd or all
		out_id 		= 'out_id' in cmd or all
		chunk		= 'chunk' in cmd
				
		if name or out_id:self.name = RPR_GetSetMediaTrackInfo_String(id, "P_NAME", "", 0)[3]
		if folder: self.folder = RPR_GetMediaTrackInfo_Value(id, "I_FOLDERDEPTH")
		if out_id: self.out_id = OUT_DAT(self.name)
		if chunk:
			maxlen 			= 1024*1024*4
			self.chunk		= RPR_GetSetTrackState(self.id, "", maxlen)[2]
		

	def select(self, cmd=''):
		RPR_SetMediaTrackInfo_Value(self.id, "I_SELECTED", 1)
		KB_UpdateView()
		
	def select_only(self, cmd=''):
		RPR_SetOnlyTrackSelected(self.id)
		KB_UpdateView()
		
	def rename(self, new_nm):
		RPR_GetSetMediaTrackInfo_String(self.id, "P_NAME", new_nm, True)
	
	def solo(self, solo=True):
		if solo:
			RPR_SetMediaTrackInfo_Value(self.id, "I_SOLO", 1)
		else:
			RPR_SetMediaTrackInfo_Value(self.id, "I_SOLO", 0)
	
			
	# ========================================================================#
	def for_(type='sel_tracks', cmd='all'):
	# =======================================================================#
		
		if 'sel_tracks' in type :
			# yield map(TD, TD.get_SelTracks())
			for i, id in TD.get_SelTracks():			
				yield TD(id, cmd, i)
			
		elif 'all_tracks' in type :
			for i, id in TD.get_Tracks():	
				yield TD(id, cmd)
				
		elif 'sel_items' in type :
			for i in range(RPR_CountSelectedMediaItems(0)) :
				yield i, RPR_GetTrackRPR_GetSelectedMediaItem(0, i)	
				
		elif 'all_items' in type :
			for i in range(track_total) :
				yield i, RPR_GetMediaItem(0, i)
				
		elif 'sel_items_on_Track' in type :
			for a_item in TD.get_SelItems_OnTrack(self.id) :
				yield i, a_item
				
		elif 'items_on_Track' in type :
				for a_item in TD.get_Items_OnTrack(self.id) :
					yield i, a_item		
					
	# ========================================================================#
	
	def get_SelTracks():        
		# for i in range(RPR_CountSelectedTracks(0)):
				# yield i, RPR_GetSelectedTrack(0,i)
		sel_ids=TD.TracksSelList()
		for i, track in enumerate(sel_ids):
				yield i, track

	def TracksSelList():return [RPR_GetSelectedTrack(0,i) for i in range(RPR_CountSelectedTracks(0))]
	
	
	def get_Tracks():        	
		for i in range(RPR_CountTracks(0)):
				yield i, RPR_GetTrack(0,i)	
									
	def get_Items_OnTrack(t):        
		for i in range(RPR_CountMediaItems(0)):
			a_item=RPR_GetMediaItem(0,i)
			if RPR_GetMediaItem_Track(a_item) == t :
				yield i, a_item
				
	def get_SelItems_OnTrack(t):        
		for i in range(RPR_CountSelectedMediaItems(0)):
			a_item=RPR_GetSelectedMediaItem(0,i)
			if RPR_GetMediaItem_Track(a_item) == t :
				yield i, a_item
# ========================================================================#
class OUT_DAT:
# ========================================================================#
	id_pt		= r'\[(\d{1,})\.(\d{1,})\]'
	combi_id_pt	= r'\[(\d{1,})\]'
	
			
	def __init__(self, name):
		# self.name			=name
		self.shrt_nm		=''
		self.combi			=re.search(OUT_DAT.combi_id_pt, name)
		self.vst_num		=''
		self.sub_num		=''
		self.id				=''
		self.search_id		=''
		self.search_sym		=[]
		self.vst_search_id=''
	
		if not self.combi and not re.search(OUT_DAT.id_pt, name):
			# msg("Couldn't find an output pattern in: " + name)
			# raise NameError(name)
			# msg("Couldn't find a left-bracket in: " + name)
			# del(self)
			return None
		
		
		if not self.combi:
			c_pt				=OUT_DAT.id_pt
			id_temp				=re.search(c_pt, name)
			self.sub_num		=id_temp.group(2)
			self.search_sym.append('{')
			self.search_sym.append('}')
		else:
			c_pt				=OUT_DAT.combi_id_pt
			id_temp				=re.search(c_pt, name)
			self.search_sym.append('{')
			self.search_sym.append('} ')

		self.id				=id_temp.group()
		self.vst_num		=id_temp.group(1)
		if self.vst_num[0:1]=='0':self.vst_num = self.vst_num[1:]
		
		self.shrt_nm		=re.sub(c_pt,"", name)
		
		self.search_id		=id_temp.group().replace('[',self.search_sym[0])
		self.search_id		=self.search_id.replace(']',self.search_sym[1])
		
		# if 14 <= int(self.vst_num) <= 15:
			# self.vst_search_id = '{' + self.vst_num + '} '
		# else: 
		self.vst_search_id = "{" + self.vst_num + "*}"
		if self.combi: self.search_id = 'Outs {' + self.vst_num + '}' 
		
		#DEBUG
		# o=str('vst_num ' + self.vst_num +'\n' +
		# 'sub_num ' + self.sub_num +'\n' +
		# 'id ' + self.id +'\n' +
		# 'shrt_nm ' + self.shrt_nm +'\n'
		# 'search_id ' + self.search_id +'\n'
		# 'vst_search_id ' + self.vst_search_id +'\n')
		# msg(o)
		

# ========================================================================#	
def KB_SearchOut_Gen(td, cmd='sub_fx|mcp') :
# ========================================================================#
	cmd					= cmd.split('|')
	vst_fx 				= 'vst_fx' in cmd
	sub_fx				= 'sub_fx' in cmd
	bump				= 'bump' in cmd
	mcp					= 'mcp' in cmd
	shw_sends			= 'shw_sends' in cmd
	sel					= 'sel' in cmd
	search_options		= ''
	fx_search			= ''
	
	# # # # # # # # # # # # # # # #
	# FETCH THE OUTPUTS:
	# # # # # # # # # # # # # # # #
	if not td.out_id:
		raise NameError("Bad/no out_id for track: " + td.name)
		yield None
	
	td.select_only()
	
	
	try:		
		# # # # # # # # # # # # # # # #
		if bump or mcp or sel:
		# # # # # # # # # # # # # # # #
			search_options += "sel|exclusive"
		
		# # # # # # # # # # # # # # # #
		if vst_fx or sub_fx and not td.out_id.combi:
		# # # # # # # # # # # # # # # #
			# Show the VSTi tracks FX chain
			if vst_fx:	
				fx_search=td.out_id.vst_search_id
			# Show the sub-output's FX chain
			elif sub_fx: 
				fx_search=td.out_id.search_id
				# msg(fx_search)
				# yield
			
			search_options+='|fxchain'
			# output_id=KB_Track_Op_New("fxchain", fx_name=fx_search)

		# msg(td.out_id.search_id)
		# return
		
		output_id=KB_Track_Op_New(td.out_id.search_id, search_options, fx_search)
		
		# Selects the children if it's a folder.
		if RPR_GetMediaTrackInfo_Value(output_id, "I_FOLDERDEPTH") >= 1 : RPR_Main_OnCommand(RPR_NamedCommandLookup('_SWS_SELCHILDREN2'), 0)
		
		# yield
		
	except NameError as e:
		raise NameError(('Could not find track for Out_ID:', str(e), 'of track: ', td.name))
		yield None
		
	# # # # # # # # # # # # # # # #
	if mcp:
	# # # # # # # # # # # # # # # #
		
		if td.i == 0:
			RPR_Main_OnCommand(RPR_NamedCommandLookup('_SWSTL_SHOWMCPEX'), 0) # Show selected track(s) in MCP, hide others
		else:
			RPR_Main_OnCommand(RPR_NamedCommandLookup('_SWSTL_SHOWMCP'), 0) # Show selected track(s) in MCP
		KB_ShowMixer()
		KB_UpdateView()
	
	# # # # # # # # # # # # # # # #
	if bump : output_id=KB_Bump_To_Track(td)
	# # # # # # # # # # # # # # # #
	
	# # # # # # # # # # # # # # # #
	if shw_sends:
	# # # # # # # # # # # # # # # #		
		# connected_tracks=KB_SelectSendsOfTrack(output_id)
		
		connected_tracks=KB_Track_SelectSends(TD.TracksSelList())
		
		# all_music_id = KB_Track_Op_New('ALL MUSIC', 'exact')
		# linked = []
		# while all_music_id not in linked:
			# linked =KB_Track_SelectSends(TD.TracksSelList())
		
		RPR_Main_OnCommand(RPR_NamedCommandLookup('_SWSTL_SHOWMCP'), 0)
		
		# for c_track in connected_tracks:
			# RPR_SetMediaTrackInfo_Value(c_track, "I_SELECTED", 0)
			
	# if bump or mcp:
		# RPR_Main_OnCommand(RPR_NamedCommandLookup("_SWS_RESTORESEL"), 0)
		# KB_UpdateView()
		# td.refresh_sel()
		
	# msg(td.name + ' DONE.')
	RPR_SetMediaTrackInfo_Value(output_id, "I_SELECTED", 0)
	KB_UpdateView()
	yield output_id
	# return output_id
