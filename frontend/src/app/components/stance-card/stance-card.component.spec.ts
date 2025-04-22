import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StanceCardComponent } from './stance-card.component';

describe('StanceCardComponent', () => {
  let component: StanceCardComponent;
  let fixture: ComponentFixture<StanceCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StanceCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StanceCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
