for f in AllFonts():
    print('Save', f.path)
    f.save()
    f.close()