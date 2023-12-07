for f in AllFonts():
    
    if 1:
        for groupName, group in f.groups.items():
            if 'omicron.cm1' in group:
                print('---')
                print(groupName, group)
    
        print('===')
        for groupName, group in f.groups.items():
            if 'omicron.cm1' in group:
                print('---')
                print(groupName, group)
    f.groups['public.kern2.Omicron_gr'] = ('Omicron', 'Omicron.alt1', 'Omicron.alt2', 'Omicron.cm0', 'Omicron.cm1', 'Omicron.cm2', 'Omicron.ct0', 'Omicron.ct1', 
    'Omicron.ct2', 'Phi', 'Phi.alt1', 'Phi.alt2', 'Theta', 'Theta.alt1', 'Theta.alt2', 'Theta.cm0', 'Theta.cm1', 'Theta.cm2', 'Theta.ct0', 'Theta.ct1', 'Theta.ct2')
    f.groups['public.kern2.omicron_gr'] = ('alpha', 'alpha.alt1', 'alpha.alt2', 'alpha.cm0', 'alpha.cm1', 'alpha.cm2', 'alpha.ct0', 'alpha.ct1', 'alpha.ct2', 
    'alphatonos', 'alphatonos.alt1', 'alphatonos.alt2', 'alphatonos.cm0', 'alphatonos.cm1', 'alphatonos.cm2', 'alphatonos.ct0', 'alphatonos.ct1', 'alphatonos.ct2', 
    'omicron', 'omicron.alt1', 'omicron.alt2', 'omicron.cm0', 'omicron.cm1', 'omicron.cm2', 'omicron.ct0', 'omicron.ct1', 'omicron.ct2', 'omicrontonos', 'omicrontonos.alt1', 
    'omicrontonos.alt2', 'omicrontonos.cm0', 'omicrontonos.cm1', 'omicrontonos.cm2', 'omicrontonos.ct0', 'omicrontonos.ct1', 'omicrontonos.ct2', 'phi', 
    'phi.alt1', 'phi.alt2', 'sigma', 'sigma.alt1', 'sigma.alt2', 'sigma.cm0', 'sigma.cm1', 'sigma.cm2', 'sigma.ct0', 'sigma.ct1', 'sigma.ct2', 'sigma1', 'sigma1.alt1', 'sigma1.alt2')

    f.save()
    f.close()
    
print('Done')