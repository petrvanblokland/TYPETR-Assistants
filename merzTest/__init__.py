
XXXUFO_FILENAMES = ( # ufo/
	#'SegoeUI-Hairline_MA32.ufo', # Source master for "lighter" interpolations.
	'SegoeUI-Light_MA98.ufo',
	'SegoeUI-SemiLight_MA133.ufo',
	'SegoeUI-Regular_MA168.ufo',
	'SegoeUI-SemiBold_MA238.ufo',
	'SegoeUI-Bold_MA323.ufo',
)
UFO_SPACE_MASTERS = {
	# ufo/												ms-original-sources/master_ufo/
	'Segoe_ASCII_UI-Regular_MA168.ufo': 				'ms-original-sources/master_ufo/SegoeUI-Regular.ufo',
	'Segoe_ASCII_UI-Light_MA98.ufo': 					'ms-original-sources/master_ufo/SegoeUI-Light.ufo',
	'Segoe_ASCII_UI-Hairline_MA32.ufo': 				None, # Just text/fix margin relations inside this ufo
	'Segoe_ASCII_UI-Bold_MA323.ufo': 					'ms-original-sources/master_ufo/SegoeUI-Bold.ufo',
	'Segoe_ASCII_UI_xHeightMax-Regular_MA168.ufo': 		None,
	'Segoe_ASCII_UI_xHeightMax-Light_MA98.ufo': 		None,
	'Segoe_ASCII_UI_xHeightMax-Hairline_MA32.ufo': 		None,
	'Segoe_ASCII_UI_xHeightMax-Bold_MA323.ufo': 		None,
	'Segoe_ASCII_Display-Regular_MA168.ufo': 			None,
	'Segoe_ASCII_Display-Light_MA98.ufo': 				None,
	'Segoe_ASCII_Display-Hairline_MA32.ufo': 			None,
	'Segoe_ASCII_Display-Bold_MA323.ufo': 				None,
}
DO = 0 # Base display offset spacing
TO = 48 # Text-offset spacing

UFO_REGULAR = 'Segoe_ASCII_UI-Regular_MA168.ufo' # Main interpolation reference

UFO_2_MASTER = {
	# ufo/												masters-ascii-V0.5/
	'Segoe_ASCII_Display-Bold_MA323.ufo': 				('Segoe_ASCII_Display-Bold_323.ufo',),
	'Segoe_ASCII_Display-Regular_MA168.ufo': 			('Segoe_ASCII_Display-Regular_168.ufo',),
	'Segoe_ASCII_Display-Light_MA98.ufo': 				('Segoe_ASCII_Display-Light_98.ufo',),
	'Segoe_ASCII_Display-Hairline_MA32.ufo': 			('Segoe_ASCII_Display-Hairline_32.ufo',),

	'Segoe_ASCII_UI-Bold_MA323.ufo': 					('Segoe_ASCII_UI-Bold_323.ufo',),
	UFO_REGULAR: 										('Segoe_ASCII_UI-Regular_168.ufo',),
	'Segoe_ASCII_UI-Light_MA98.ufo': 					('Segoe_ASCII_UI-Light_98.ufo',
									 					 'Segoe_ASCII_UI-Hairline_32.ufo'),

	#'Segoe_ASCII_Display_xHeightMax-Bold_MA323.ufo': 	('Segoe_ASCII_Display_xHeightMax-Bold_323.ufo',),
	#'Segoe_ASCII_Display_xHeightMax-Regular_MA168.ufo': ('Segoe_ASCII_Display_xHeightMax-Regular_168.ufo',),
	#'Segoe_ASCII_Display_xHeightMax-Light_MA98.ufo': 	('Segoe_ASCII_Display_xHeightMax-Light_98.ufo',
	#												  	 'Segoe_ASCII_Display_xHeightMax-Hairline_32.ufo'),

	'Segoe_ASCII_UI_xHeightMax-Bold_MA323.ufo': 		('Segoe_ASCII_UI_xHeightMax-Bold_323.ufo',),
	'Segoe_ASCII_UI_xHeightMax-Regular_MA168.ufo': 		('Segoe_ASCII_UI_xHeightMax-Regular_168.ufo',),
	'Segoe_ASCII_UI_xHeightMax-Light_MA98.ufo': 		('Segoe_ASCII_UI_xHeightMax-Light_98.ufo',
														 'Segoe_ASCII_UI_xHeightMax-Hairline_32.ufo'),

}
UFO_ASCII_FILENAMES = { # ufo-control/
	#'SegoeUI_Control_Display-Regular_MA168.ufo', # Original

	# Design 3
	'Segoe_ASCII_Display-Bold_323.ufo': dict(stem=323, xStem=316, capHeight=1434, xHeight=1024, marginOffset=DO), 
    #'Segoe_ASCII_Display-SemiBold_238.ufo': dict(stem=238, xStem=232, capHeight=1434, xHeight=1024, marginOffset=DO-2), 
	'Segoe_ASCII_Display-Regular_168.ufo': dict(stem=168, xStem=163, capHeight=1434, xHeight=1024, marginOffset=DO-4), 
    #'Segoe_ASCII_Display-SemiLight_133.ufo': dict(stem=133, xStem=128, capHeight=1434, xHeight=1024, marginOffset=DO-6),
	'Segoe_ASCII_Display-Light_98.ufo': dict(stem=98, xStem=92, capHeight=1434, xHeight=1024, marginOffset=DO-8), 
    'Segoe_ASCII_Display-Hairline_32.ufo': dict(stem=32, xStem=31, capHeight=1434, xHeight=1024, marginOffset=DO-10),

    # Design 1
    'Segoe_ASCII_UI-Bold_323.ufo': dict(stem=323, xStem=316, capHeight=1434, xHeight=1024, marginOffset=0),
    #'Segoe_ASCII_UI-SemiBold_238.ufo': dict(stem=238, xStem=232, capHeight=1434, xHeight=1024, marginOffset=0),
    'Segoe_ASCII_UI-Regular_168.ufo': dict(stem=168, xStem=163, capHeight=1434, xHeight=1024, marginOffset=0), # Original
    #'Segoe_ASCII_UI-SemiLight_133.ufo': dict(stem=133, xStem=128, capHeight=1434, xHeight=1024, marginOffset=0),
    'Segoe_ASCII_UI-Light_98.ufo': dict(stem=98, xStem=92, capHeight=1434, xHeight=1024, marginOffset=0),
    'Segoe_ASCII_UI-Hairline_32.ufo': dict(stem=32, xStem=31, capHeight=1434, xHeight=1024, marginOffset=0),

    # Design 3
	'Segoe_ASCII_Display_xHeightMax-Bold_323.ufo': dict(stem=323, xStem=316, capHeight=1434, xHeight=1228, marginOffset=DO), 
    #'Segoe_ASCII_Display_xHeightMax-SemiBold_238.ufo': dict(stem=238, xStem=232, capHeight=1434, xHeight=1228, marginOffset=DO-2), 
	'Segoe_ASCII_Display_xHeightMax-Regular_168.ufo': dict(stem=168, xStem=163, capHeight=1434, xHeight=1228, marginOffset=DO-4), 
    #'Segoe_ASCII_Display_xHeightMax-SemiLight_133.ufo': dict(stem=133, xStem=128, capHeight=1434, xHeight=1228, marginOffset=DO-6), 
	'Segoe_ASCII_Display_xHeightMax-Light_98.ufo': dict(stem=98, xStem=92, capHeight=1434, xHeight=1228, marginOffset=DO-8), 
	'Segoe_ASCII_Display_xHeightMax-Hairline_32.ufo': dict(stem=32, xStem=31, capHeight=1434, xHeight=1228, marginOffset=DO-10), 

	# Design 1
    'Segoe_ASCII_UI_xHeightMax-Bold_323.ufo': dict(stem=323, xStem=316, capHeight=1434, xHeight=1228, marginOffset=0),
    'Segoe_ASCII_UI_xHeightMax-SemiBold_238.ufo': dict(stem=238, xStem=232, capHeight=1434, xHeight=1228, marginOffset=0),
    'Segoe_ASCII_UI_xHeightMax-Regular_168.ufo': dict(stem=168, xStem=163, capHeight=1434, xHeight=1228, marginOffset=0), # Original
    'Segoe_ASCII_UI_xHeightMax-SemiLight_133.ufo': dict(stem=133, xStem=128, capHeight=1434, xHeight=1228, marginOffset=0),
    'Segoe_ASCII_UI_xHeightMax-Light_98.ufo': dict(stem=98, xStem=92, capHeight=1434, xHeight=1228, marginOffset=0),
    'Segoe_ASCII_UI_xHeightMax-Hairline_32.ufo': dict(stem=32, xStem=31, capHeight=1434, xHeight=1228, marginOffset=0),
}
# Text masters generated automatic by Segoe-weight5-interpolate-to-text8pt.designspace
# Exported to _export-masters-ascii-V0.5/
MASTER_TEXT_FILENAMES = {
	'Segoe_ASCII_Text-Bold_300.ufo': dict(marginOffset=TO), # Double from normal, em=2048
	#'Segoe_ASCII_Text-SemiBold.ufo': dict(marginOffset=TO),
	'Segoe_ASCII_Text-Regular_200.ufo': dict(marginOffset=TO),
	#'Segoe_ASCII_Text-SemiLight.ufo': dict(marginOffset=TO),
	'Segoe_ASCII_Text-Light_160.ufo': dict(marginOffset=TO),
}
# Exported to _export-masters-ascii-V0.5/
MASTER_DISPLAY_FILENAMES = {
	'Segoe_ASCII_Display-Bold_323.ufo': dict(marginOffset=DO), # Double from normal, em=2048
	#'Segoe_ASCII_Display-SemiBold.ufo': dict(marginOffset=DO-2),
	'Segoe_ASCII_Display-Regular_168.ufo': dict(marginOffset=DO-4),
	#'Segoe_ASCII_Display-SemiLight.ufo': dict(marginOffset=DO-6),
	'Segoe_ASCII_Display-Light_64.ufo': dict(marginOffset=DO-8),
}

