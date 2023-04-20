import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  isLoading = false;
  errorMsg = '';

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit(): void {
    const userData = {
      username: this.username,
      password: this.password
    };
    this.isLoading = true;

    this.http.post('http://localhost:8000/api/token/', userData).subscribe(
      (response: any) => {
        this.isLoading = false;
        localStorage.setItem('access', response.access);
        localStorage.setItem('refresh', response.refresh);
        this.router.navigate(['/scan-form']);
      },
      (error) => {
        this.isLoading = false;
        this.errorMsg = 'Invalid username or password';
      }
    );
  }
}

