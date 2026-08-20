# Feedback-event test coverage

The local suite covers:

1. valid baseline;
2. duplicate event ID rejection;
3. hash-chain tamper rejection;
4. future predecessor rejection;
5. silent evidence downgrade rejection;
6. evidence-backed correction acceptance;
7. claim promotion without gate rejection;
8. claim promotion with gate and evidence acceptance.

Local observed result: `8/8 PASS`. Remote CI remains separately observable.
