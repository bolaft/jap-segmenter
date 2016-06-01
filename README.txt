# Install Wapiti
in ./Wapiti
	make
	make install

# Baseline
python hmm_segmenter.py data/knbc-train.xml data/knbc-test.xml knbc-hmm.xml

# ML segmenter
python ml_segmenter.py data/knbc-train.xml data/knbc-test.xml knbc-ml.xml

# Evaluation
python evaluation.py knbc-ml.xml data/knbc-reference.xml

# Baseline (hmm_segmenter) scores :
Avg Precision 0.904005681695
Avg Recall 0.881382517888
Avg f-measure 0.892550767507

# ML scores :
Avg Precision 0.971283959698
Avg Recall 0.971952337787
Avg f-measure 0.971618033798
