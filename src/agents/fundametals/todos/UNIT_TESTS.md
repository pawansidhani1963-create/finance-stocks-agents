## Unit Testing & Validation

### Statement Retrieval
- [ ] Unit tests for income statement normalization
- [ ] Unit tests for balance sheet normalization
- [ ] Unit tests for cash flow normalization

### Derived Metrics
- [ ] Test binary_addition
- [ ] Test binary_subtraction
- [ ] Test ratio derivation
- [ ] Test missing input handling
- [ ] Test division-by-zero protection

### Period Logic
- [ ] Test discrete vs YTD detection
- [ ] Test amendment override logic
- [ ] Test most recent filing detection

### Integration Tests
- [ ] End-to-end test for full ticker processing
- [ ] Validate metadata freshness logic
- [ ] Validate recompute trigger behavior

### Setup Test Covergage
- [ ] Add some framework to test how much code is correctly tested and how much is the test coverage
- [ ] If possible add it in the build process so that we can see this information at build time

Goal:
Guarantee deterministic correctness and prevent silent financial errors.