
:: nmt/scripts/download_iwslt15.sh tmp/nmt_data
:: mkdir tmp/nmt_model

:TrainGPU

python -m nmt.nmt ^
    --src=en --tgt=ar ^
    --vocab_prefix=Data/Ted2013/vcbTED2013.ar-en ^
    --train_prefix=Data/Ted2013/srcTED2013.ar-en ^
    --dev_prefix=Data/Ted2013/vldTED2013.ar-en ^
    --test_prefix=Data/Ted2013/tstTED2013.ar-en ^
    --out_dir=Data/Ted2013/nmt_model ^
    --num_train_steps=24000 ^
    --steps_per_stats=100 ^
    --batch_size=128 ^
    --num_layers=2 ^
    --num_units=128 ^
    --dropout=0.2 ^
    --metrics=bleu

:DONE
echo "Done!"