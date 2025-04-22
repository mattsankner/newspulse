import { TestBed } from '@angular/core/testing';

import { StanceService } from './stance.service';

describe('StanceService', () => {
  let service: StanceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StanceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
