
mkdir venv

python -m venv venv --prompt=KernNet

source venv/bin/activate

pip install --upgrade pip

pip install torch torchvision torchaudio
pip install pandas
pip install tqdm
pip install pillow
pip install numpy
pip install rasterio

pip install defcon
pip install fontbakery
pip install fontmake
pip install fontparts
pip install statmake
pip install ttfautohint-py
pip install fontPens
pip install ufo2ft

pip install brotli
pip install git+https://github.com/typemytype/drawbot

* fontmake -o ttf --output-dir ttf -u ufo/Presti*.ufo
* fontmake -o otf --output-dir otf -u ufo/Presti*.ufo
* ttx -d ttf/ttx/ ttf/*.ttf
* ttx -d _ttf/ttx/ _ttf/*.ttf
* fontmake -o otf --output-dir ../_otf/ -u ../_instances/Presti*.ufo

# Run this parallel to assistants that use spacer.py part.
cd assistantLib/kernnet7
python kernNetServer-007.py
