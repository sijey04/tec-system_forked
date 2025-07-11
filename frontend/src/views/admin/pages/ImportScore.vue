<template>
  <div class="min-h-screen bg-gray-50 py-4">
    <div class="container mx-auto px-4 max-w-7xl">
      <!-- Header Section -->
      <div class="mb-4">
        <div class="flex items-center space-x-3">
          <div class="p-2 bg-crimson-100 rounded-lg">
            <i class="fas fa-file-contract text-2xl text-crimson-600"></i>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Admin: Import Exam Scores</h1>
            <p class="text-sm text-gray-600">Upload and import individual examination scores for different exam types. Scores will be available to registered users.</p>
          </div>
        </div>
      </div>

      <!-- Error message with login button -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
        <div class="flex flex-col sm:flex-row sm:items-center gap-3">
          <div class="flex items-center">
            <i class="fas fa-exclamation-circle text-red-500 mr-2"></i>
            <p class="text-red-700">{{ error }}</p>
          </div>
          <a href="/admin/login" class="inline-flex items-center px-4 py-2 bg-crimson-600 text-white rounded-lg text-sm hover:bg-crimson-700 transition-colors">
            <i class="fas fa-sign-in-alt mr-2"></i>
            Go to Login
          </a>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <!-- Upload Section -->
        <div class="lg:col-span-8">
          <div class="bg-white rounded-lg shadow p-4">
            <div class="mb-4">
              <div class="flex items-center justify-between mb-2">
                <h2 class="text-lg font-semibold text-gray-900">Upload Score File</h2>
                <span class="text-sm px-2 py-1 bg-blue-50 text-blue-700 rounded-full">Step 1 of 2</span>
              </div>
              <p class="text-sm text-gray-600 mb-3">Upload your CSV or Excel file containing the exam scores</p>
              
              <!-- File Upload Area -->
              <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-crimson-500 transition-all duration-200 cursor-pointer"
                   @dragover.prevent="dragover = true"
                   @dragleave.prevent="dragover = false"
                   @drop.prevent="onFileDrop"
                   :class="{ 'border-crimson-500 bg-crimson-50/30': dragover }"
                   @click="$refs.fileInput.click()">
                <div class="space-y-3">
                  <div class="w-16 h-16 mx-auto bg-crimson-50 rounded-full flex items-center justify-center transform transition-transform duration-200"
                       :class="{ 'scale-110': dragover }">
                    <i class="fas fa-file-upload text-2xl text-crimson-600"></i>
                  </div>
                  <div>
                    <p class="text-sm text-gray-600">Drag and drop your file here, or</p>
                    <label class="mt-2 inline-flex items-center px-4 py-2 bg-crimson-600 text-white rounded-lg hover:bg-crimson-700 transition-colors duration-200 cursor-pointer text-sm">
                      <i class="fas fa-folder-open mr-2"></i>
                      Browse Files
                      <input ref="fileInput" type="file" class="hidden" accept=".csv,.xlsx,.xls" @change="onFileSelect">
                    </label>
                    <p class="mt-2 text-sm text-gray-500">Supported formats: CSV, Excel (.xlsx, .xls)</p>
                  </div>
                </div>
              </div>
              
              <!-- File preview if selected -->
              <div v-if="selectedFile" class="mt-3 p-3 bg-gray-50 rounded-lg flex items-center justify-between animate-fade-in">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center">
                    <i class="fas fa-file-excel text-green-600 text-xl"></i>
                  </div>
                  <div>
                    <p class="font-medium text-sm text-gray-900">{{ selectedFile.name }}</p>
                    <p class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
                  </div>
                </div>
                <button @click.stop="selectedFile = null" 
                        class="p-2 text-gray-500 hover:text-crimson-600 hover:bg-gray-100 rounded-lg transition-colors duration-200">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>

            <!-- Import Settings -->
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <h3 class="text-base font-semibold text-gray-900">Import Settings</h3>
                <span class="text-sm px-2 py-1 bg-blue-50 text-blue-700 rounded-full">Step 2 of 2</span>
              </div>
              
              <!-- Exam Type Selection -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Select Exam Type</label>
                <select v-model="selectedExamType" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-crimson-500 focus:border-crimson-500 transition-colors duration-200 text-sm"
                        @change="updateSelectedProgramId">
                  <option value="">Choose an exam type</option>
                  <option v-for="exam in examTypes" :key="exam.value" :value="exam.value">{{ exam.label }}</option>
                </select>
                <p v-if="selectedProgramId" class="mt-1 text-xs text-green-600">
                  <i class="fas fa-check-circle mr-1"></i>
                  Program ID: {{ selectedProgramId }} (Will be used to match appointments)
                </p>
                <p v-else-if="selectedExamType" class="mt-1 text-xs text-amber-600">
                  <i class="fas fa-exclamation-circle mr-1"></i>
                  No program ID found for this exam type. Matching might be less accurate.
                </p>
              </div>

              <!-- Exam Year Selection -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Select Exam Year</label>
                <select v-model="selectedExamYear" 
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-crimson-500 focus:border-crimson-500 transition-colors duration-200 text-sm">
                  <option value="">Choose an exam year</option>
                  <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
                </select>              </div>
              
              <!-- Validation Message -->
              <div v-if="!isReadyToImport && missingFields.length > 0" 
                   class="text-amber-600 text-sm py-1 flex items-center">
                <i class="fas fa-exclamation-circle mr-1"></i>
                {{ validationMessage }}
              </div>

              <!-- Import Button -->
              <div class="pt-2">
                <button 
                  @click="startImport"
                  :disabled="!isReadyToImport"
                  :class="[
                    'w-full px-4 py-2.5 rounded-lg flex items-center justify-center space-x-2 transition-all duration-200 text-sm',
                    isReadyToImport 
                      ? 'bg-crimson-600 text-white hover:bg-crimson-700 hover:shadow-md' 
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  ]">
                  <i class="fas fa-upload"></i>
                  <span>Start Import</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Import History & Guidelines -->
        <div class="lg:col-span-4 space-y-4">
          <!-- Import Guidelines -->
          <div class="bg-white rounded-lg shadow p-4">
            <div class="flex items-center space-x-3 mb-3">
              <div class="p-2 bg-crimson-100 rounded-lg">
                <i class="fas fa-info-circle text-crimson-600 text-lg"></i>
              </div>
              <h2 class="text-base font-semibold text-gray-900">Import Guidelines</h2>
            </div>
            <div class="space-y-3">
              <div class="flex items-start space-x-3">
                <div class="w-6 h-6 rounded-full bg-crimson-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <i class="fas fa-info text-crimson-600 text-sm"></i>
                </div>
                <p class="text-sm text-gray-600">Your file should include all test part scores and identifiers (name fields, school, and app_no are required)</p>
              </div>
              <div class="flex items-start space-x-3">
                <div class="w-6 h-6 rounded-full bg-crimson-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <i class="fas fa-table text-crimson-600 text-sm"></i>
                </div>
                <p class="text-sm text-gray-600">CSV columns: app_no, lastname, firstname, middlename, school, date, part1, part2, part3, part4, part5, oapr</p>
              </div>
              <div class="flex items-start space-x-3">
                <div class="w-6 h-6 rounded-full bg-crimson-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <i class="fas fa-font text-crimson-600 text-sm"></i>
                </div>
                <p class="text-sm text-gray-600">All text data in columns (lastname, firstname, middlename, school) must be CAPITALIZED for easy parsing</p>
              </div>
              
              <!-- Sample CSV Format -->
              <div class="rounded-md bg-gray-50 p-3 border border-gray-200 text-xs font-mono overflow-x-auto whitespace-nowrap">
                app_no,lastname,firstname,middlename,school,date,part1,part2,part3,part4,part5,oapr<br>
                123-456,DOE,JOHN,ANTONIO,SAMPLE SCHOOL,2023-10-15,85,92,88,95,90,90<br>
                789-012,SMITH,JANE,MARIE,TEST ACADEMY,2023-10-15,92,88,90,87,94,92
              </div>
            </div>
          </div>

          <!-- Recent Imports -->
          <div class="bg-white rounded-lg shadow p-4">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <div class="p-2 bg-crimson-100 rounded-lg">
                  <i class="fas fa-history text-crimson-600 text-lg"></i>
                </div>
                <h2 class="text-base font-semibold text-gray-900">Recent Score Imports</h2>
              </div>
              <button class="text-sm text-blue-600 hover:text-blue-800">View All</button>
            </div>
            <div class="space-y-2">
              <div v-for="(import_, index) in recentImports" :key="index" 
                   class="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-900">{{ import_.examType }}</span>
                  <span class="text-sm text-gray-500">{{ import_.date }}</span>
                </div>
                <div class="flex items-center space-x-3 text-sm mt-1">
                  <span class="text-green-600 bg-green-50 px-2 py-1 rounded-full">
                    <i class="fas fa-check-circle mr-1"></i>
                    {{ import_.successful }}
                  </span>
                  <span class="text-red-600 bg-red-50 px-2 py-1 rounded-full">
                    <i class="fas fa-times-circle mr-1"></i>
                    {{ import_.failed }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add loading state -->
      <div v-if="loading" class="text-center py-4">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-crimson-600 border-t-transparent"></div>
        <p class="mt-2 text-gray-600">Loading program codes...</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from '../../../composables/useToast';

export default {
  name: 'ImportScore',
  setup() {
    const { showToast } = useToast();
    return { showToast };
  },
  data() {
    return {
      dragover: false,
      selectedFile: null,
      selectedExamType: '',
      selectedExamYear: '',
      selectedProgramId: null, // Store the program ID associated with the selected exam type
      examTypes: [], // Will be populated from backend with program ID mapping
      programMapping: {}, // Map from exam type code to program ID
      availableYears: [], // Will be populated based on the current year
      loading: false,
      error: null,
      sessionId: null, // Will store session ID if passed from TestSessionManagement
      recentImports: [
        {
          examType: 'LSAT Exam',
          date: '2024-03-15 14:30',
          successful: 120,
          failed: 2
        },
        {
          examType: 'NAT Exam',
          date: '2024-03-14 16:45',
          successful: 180,
          failed: 3
        },
        {
          examType: 'EAT Exam',
          date: '2024-03-13 09:15',
          successful: 150,
          failed: 1
        }
      ]
    }
  },  computed: {
    isReadyToImport() {
      return this.selectedFile && this.selectedExamType && this.selectedExamYear;
    },
    missingFields() {
      const missing = [];
      if (!this.selectedFile) missing.push('CSV or Excel file');
      if (!this.selectedExamType) missing.push('exam type');
      if (!this.selectedExamYear) missing.push('exam year');
      return missing;
    },
    validationMessage() {
      if (this.missingFields.length > 0) {
        return `Please select ${this.missingFields.join(' and ')} before importing.`;
      }
      return '';
    }
  },
  methods: {
    async checkAuthStatus() {
      const token = localStorage.getItem('token') || 
                   localStorage.getItem('access_token') || 
                   localStorage.getItem('authToken');
      
      if (!token) {
        this.error = 'You must be logged in to import exam scores. Please log in to your admin account first.';
        return false;
      }
      
      try {
        // Try to access a protected endpoint to verify token is valid
        const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
        const apiUrlWithoutTrailingSlash = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
        
        // Just return true for now since we have a token
        // The actual API call validation can be done when making the import request
        return true;
      } catch (error) {
        console.error('Auth error:', error);
        if (error.response && error.response.status === 401) {
          this.error = 'Your session has expired. Please log in again.';
          // Clear invalid tokens
          localStorage.removeItem('token');
          localStorage.removeItem('access_token');
          localStorage.removeItem('authToken');
        } else {
          this.error = 'Authentication error. Please try logging in again.';
        }
        return false;
      }
    },    async fetchProgramCodes() {
      this.loading = true;
      this.error = null;
      
      try {
        // Use a dynamic API URL based on environment
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const apiUrlWithoutTrailingSlash = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
        
        console.log(`Fetching programs from ${apiUrlWithoutTrailingSlash}/api/programs/`);
        
        // Try different possible API endpoints
        let response = null;
        let lastError = null;
        
        try {
          response = await axios.get(`${apiUrlWithoutTrailingSlash}/api/programs/`);
        } catch (error) {
          console.log('First attempt failed:', error);
          lastError = error;
          
          try {
            // Try without /api/ prefix as fallback
            response = await axios.get(`${apiUrlWithoutTrailingSlash}/programs/`);
          } catch (error) {
            console.log('Second attempt failed:', error);
            lastError = error;
          }
        }
        
        if (!response) {
          throw lastError || new Error('Failed to fetch program codes');
        }
        
        console.log('API Response:', response.data); // Debug log
        
        // Process the API response
        if (Array.isArray(response.data)) {
          // Store both code and program ID
          this.examTypes = response.data.map(program => ({
            value: program.code,
            label: `${program.code} - ${program.name}`,
            programId: program.id
          }));
          
          // Create mapping from exam type code to program ID
          this.programMapping = {};
          response.data.forEach(program => {
            this.programMapping[program.code] = program.id;
            console.log(`Mapped ${program.code} to program ID ${program.id}`);
          });
        } else if (response.data.results && Array.isArray(response.data.results)) {
          // Handle paginated response
          this.examTypes = response.data.results.map(program => ({
            value: program.code,
            label: `${program.code} - ${program.name}`,
            programId: program.id
          }));
          
          // Create mapping from exam type code to program ID
          this.programMapping = {};
          response.data.results.forEach(program => {
            this.programMapping[program.code] = program.id;
            console.log(`Mapped ${program.code} to program ID ${program.id}`);
          });
        } else {
          console.error('Unexpected response format:', response.data);
          
          // Fallback to static exam types if API response format is unexpected
          this.examTypes = [
            { value: 'CET', label: 'CET - College Entrance Test', programId: null },
            { value: 'NAT', label: 'NAT - National Achievement Test', programId: null },
            { value: 'LSAT', label: 'LSAT - Law School Admission Test', programId: null },
            { value: 'EAT', label: 'EAT - Engineering Aptitude Test', programId: null },
            { value: 'MAT', label: 'MAT - Medical Admission Test', programId: null }
          ];
          
          this.error = 'Warning: Using default exam types. Server returned invalid format.';
        }
        
        // If we have a selected exam type, update the program ID
        if (this.selectedExamType) {
          this.updateSelectedProgramId();
        }
      } catch (error) {
        console.error('Error fetching program codes:', error);
        
        // Set appropriate error message
        if (error.response) {
          console.error('Error response:', error.response.data);
          console.error('Error status:', error.response.status);
          this.error = `Server error: ${error.response.status} - ${error.response.data.error || 'Unknown error'}`;
        } else if (error.request) {
          console.error('No response received:', error.request);
          this.error = 'No response from server. Using default exam types.';
        } else {
          console.error('Error setting up request:', error.message);
          this.error = 'Error setting up request. Using default exam types.';
        }
        
        // Fallback to static exam types
        this.examTypes = [
          { value: 'CET', label: 'CET - College Entrance Test', programId: null },
          { value: 'NAT', label: 'NAT - National Achievement Test', programId: null },
          { value: 'LSAT', label: 'LSAT - Law School Admission Test', programId: null },
          { value: 'EAT', label: 'EAT - Engineering Aptitude Test', programId: null },
          { value: 'MAT', label: 'MAT - Medical Admission Test', programId: null }
        ];
      } finally {
        this.loading = false;
      }
    },
    onFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.validateAndSetFile(file);
      }
    },
    onFileDrop(event) {
      this.dragover = false;
      const file = event.dataTransfer.files[0];
      if (file) {
        this.validateAndSetFile(file);
      }
    },
    validateAndSetFile(file) {
      // Check file type
      const validTypes = ['.csv', '.xlsx', '.xls'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!validTypes.includes(fileExtension)) {
        alert('Invalid file type. Please upload a CSV or Excel file.');
        return;
      }
      
      // Check file size (10MB limit)
      const maxSize = 10 * 1024 * 1024; // 10MB in bytes
      if (file.size > maxSize) {
        alert('File is too large. Maximum size is 10MB.');
        return;
      }
      
      this.selectedFile = file;
    },
    updateSelectedProgramId() {
      // Reset the program ID if no exam type is selected
      if (!this.selectedExamType) {
        this.selectedProgramId = null;
        return;
      }
      
      console.log('Updating program ID for exam type:', this.selectedExamType);
      console.log('Program mapping:', this.programMapping);
      console.log('Exam types:', this.examTypes);
      
      // Try to find the program ID from the mapping first
      if (this.programMapping && this.programMapping[this.selectedExamType]) {
        this.selectedProgramId = this.programMapping[this.selectedExamType];
        console.log(`Selected exam type: ${this.selectedExamType}, mapped to program ID: ${this.selectedProgramId}`);
        return;
      }
      
      // If not found in the mapping, look directly in the examTypes array
      const matchingExam = this.examTypes.find(exam => exam.value === this.selectedExamType);
      if (matchingExam && matchingExam.programId) {
        this.selectedProgramId = matchingExam.programId;
        console.log(`Found program ID ${this.selectedProgramId} directly from examTypes array`);
        return;
      }
      
      // If still not found, log a warning and set to null
      console.warn(`Could not find program ID for exam type: ${this.selectedExamType}`);
      this.selectedProgramId = null;
      
      // If we couldn't find a program ID, try to fetch programs again
      if (!this.selectedProgramId) {
        console.log('No program ID found, trying to fetch programs again...');
        this.fetchProgramCodes();
      }
    },
    formatFileSize(bytes) {
      if (bytes < 1024) {
        return bytes + ' B';
      } else if (bytes < 1024 * 1024) {
        return (bytes / 1024).toFixed(2) + ' KB';
      } else {
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
      }
    },
    async startImport() {
      if (!this.isReadyToImport) {
        return;
      }
      
      this.loading = true;
      this.error = null;
      
      // Verify authentication first
      const isAuthenticated = await this.checkAuthStatus();
      if (!isAuthenticated) {
        this.loading = false;
        return;
      }
      
      // Send data to backend API
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const apiUrlWithoutTrailingSlash = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
      const token = localStorage.getItem('token') || 
                   localStorage.getItem('access_token') || 
                   localStorage.getItem('authToken');
      
      // Create FormData to upload the file
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('examType', this.selectedExamType);
      formData.append('examYear', this.selectedExamYear);
      
      // Add program_id if available
      if (this.selectedProgramId) {
        // Make sure it's a string - the Django REST framework expects string values in FormData
        formData.append('program_id', String(this.selectedProgramId));
        console.log(`Including program_id ${this.selectedProgramId} in import request`);
      } else {
        // Warning message but continue with import
        console.warn('No program ID available for the selected exam type. Scores may not be properly categorized.');
        this.showToast('Warning: No program ID found for the selected exam type. Scores may not be properly categorized.', 'warning');
      }
      
      // Add file structure information for the backend
      const fileStructure = 'app_no,lastname,firstname,middlename,school,date,part1,part2,part3,part4,part5,oapr';
      formData.append('file_structure', fileStructure); 
      formData.append('has_headers', 'true');
      
      // Debug the form data
      for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${key === 'file' ? value.name : value}`);
      }
      
      console.log('Sending import with structure:', fileStructure);
      
      try {
        // Try multiple URLs in sequence - from most specific to most general
        const urls = [
          `${apiUrlWithoutTrailingSlash}/api/appointments/import-scores/`,
          `${apiUrlWithoutTrailingSlash}/api/admin/import-scores/`,
          `${apiUrlWithoutTrailingSlash}/api/import-scores/`,
          `${apiUrlWithoutTrailingSlash}/api/score-import/`
        ];
        
        console.log(`Trying multiple URL endpoints for score import...`);
        
        // Get the most up-to-date token
        let accessToken = localStorage.getItem('access_token') || 
                         localStorage.getItem('token') || 
                         localStorage.getItem('authToken');
        
        // Check if token needs Bearer prefix
        if (accessToken && !accessToken.startsWith('Bearer ')) {
          accessToken = `Bearer ${accessToken}`;
        }
        
        console.log('Using authorization: ', accessToken ? 'Token present' : 'No token');
        
        // Try each URL until one works
        let response = null;
        let lastError = null;
        
        for (const url of urls) {
          try {
            console.log(`Trying URL: ${url}`);
            response = await axios.post(
              url, 
              formData,
              {
                headers: {
                  'Authorization': accessToken || '',
                  'Content-Type': 'multipart/form-data'
                },
                withCredentials: true
              }
            );
            console.log(`Success with URL: ${url}`, response.data);
            break; // Exit the loop if successful
          } catch (error) {
            console.error(`Failed with URL ${url}:`, error);
            console.log('Error response:', error.response?.data);
            lastError = error;
            // Continue to next URL
          }
        }
        
        // If none of the URLs worked, throw the last error
        if (!response) {
          if (lastError && lastError.response && lastError.response.status === 403) {
            this.error = 'You do not have permission to import scores. Please log in with an admin account.';
            this.showToast(this.error, 'error');
            throw new Error('Authorization required');
          } else {
            throw lastError || new Error('All API endpoints failed');
          }
        }
        
        // If we reach here, we have a successful response
        
        console.log('Data successfully sent to API:', response.data);
        
        // Add to recent imports
        const newImport = {
          examType: this.selectedExamType,
          date: new Date().toLocaleString(),
          successful: response.data.matched + response.data.updated,
          failed: response.data.unmatched
        };
        
        this.recentImports.unshift(newImport);
        
        this.showToast(`Successfully imported ${response.data.matched} score records. ${response.data.unmatched} records were unmatched.`, 'success');
        
      } catch (apiError) {
        console.error('API storage failed:', apiError);
        
        // More detailed error message
        let errorMessage = 'Failed to save score data to the server';
        
        if (apiError.response?.data) {
          if (typeof apiError.response.data === 'string') {
            errorMessage += ': ' + apiError.response.data;
          } else if (apiError.response.data.error) {
            errorMessage += ': ' + apiError.response.data.error;
          } else if (apiError.response.data.detail) {
            errorMessage += ': ' + apiError.response.data.detail;
          }
        } else if (apiError.message) {
          errorMessage += ': ' + apiError.message;
        }
        
        this.error = errorMessage;
        this.showToast(errorMessage, 'error');
      } finally {
        this.loading = false;
      }
    }
  },  created() {
    this.fetchProgramCodes();
    
    // Generate available years (current year down to 2020)
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 2020; year--) {
      this.availableYears.push(year);
    }
    
    // Check for session ID and exam type in the URL query parameters
    const sessionId = this.$route.query.sessionId;
    const examType = this.$route.query.examType;
    
    if (sessionId) {
      console.log(`Import page loaded with sessionId: ${sessionId}, examType: ${examType}`);
      
      // If exam type was provided, pre-select it
      if (examType) {
        this.selectedExamType = examType;
      }
      
      // Store the session ID for use during import
      this.sessionId = sessionId;
    }
  },
  mounted() {
    // Check for authentication when component mounts
    this.checkAuthStatus();
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>