import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-scan-form',
  templateUrl: './scan-form.component.html',
  styleUrls: ['./scan-form.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class ScanFormComponent {
  scanName = '';
  description = '';
  target = '';
  schedule = '';
  email = '';
  isLoading = false;

  constructor(private http: HttpClient) {}

  onSubmit(): void {
    const scanData = {
      scanName: this.scanName,
      description: this.description,
      target: this.target,
      schedule: this.schedule,
      email: this.email,
    };
    this.isLoading = true;
  
    // Retrieve the access token from the localStorage
    const accessToken = localStorage.getItem('access');
  
    // Include the access token in the Authorization header
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    };
  
    this.http.post('http://localhost:8000/scan/', scanData, { headers }).subscribe(
      (response) => {
        this.isLoading = false;
        console.log(response);
        alert('Scan created and run successfully');
      },
      (error) => {
        this.isLoading = false;
        console.error(error);
        alert('Error occurred while creating the scan');
      }
    );
  }
}

