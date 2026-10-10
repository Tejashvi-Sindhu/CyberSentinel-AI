# Project architecture

CyberSentinel AI is a small, modular educational pipeline:

1. **Input validation** checks the uploaded CSV and its columns.
2. **Preprocessing** cleans missing and non-finite values.
3. **Classification** estimates whether network-flow records resemble labelled benign or attack examples.
4. **Anomaly detection** flags records that differ from a reference distribution.
5. **Risk prioritisation** combines model signals into a review score.
6. **Dashboard** visualises findings and exports analysed records.

The demo mode uses synthetic data to test application flow. Do not interpret demo metrics as real-world effectiveness.
