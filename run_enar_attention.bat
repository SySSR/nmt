


:TrainGPU

mkdir Data/Ted2013/nmt_attention_model

python -m nmt.nmt ^
    --attention=scaled_luong ^
    --src=en --tgt=ar ^
    --vocab_prefix=Data/Ted2013/vcbTED2013.ar-en ^
    --train_prefix=Data/Ted2013/srcTED2013.ar-en ^
    --dev_prefix=Data/Ted2013/vldTED2013.ar-en ^
    --test_prefix=Data/Ted2013/tstTED2013.ar-en ^
    --out_dir=Data/Ted2013/nmt_attention_model ^
    --num_train_steps=12000 ^
    --steps_per_stats=100 ^
    --batch_size=32 ^
    --num_layers=2 ^
    --num_units=128 ^
    --dropout=0.2 ^
    --metrics=bleu

:DONE
echo "Done!"