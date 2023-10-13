import drawBot

kernImagePath = '/'.join(__file__.split('/')[:-1]) + '/assistantLib/kernnet/_imagePredict/test.png'
W = H = 32
R = 12
R2 = 2*R
drawBot.newDrawing()
drawBot.newPage(W, H)
drawBot.fill(0)
drawBot.oval(-R, H/2-R, R2, R2)
drawBot.oval(W-R, H/2-R, R2, R2)
drawBot.saveImage(kernImagePath)
