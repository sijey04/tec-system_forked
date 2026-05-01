<template>
  <div class="bg-gray-100 py-8 min-h-screen" :class="{ 'py-0': popupMode, 'hidden-for-pdf-generation': outputPdfOnly }">
    <div class="form-container mx-auto shadow print:shadow-none" ref="formContainer">
      <div class="form-bg-wrap">
        <img
          src="@/assets/images/CET Application Form_page-0001.jpg"
          alt="WMSU CET Application Form"
          class="form-bg"
        >
        <div class="form-overlay">
          <span class="field field-name field-tight">{{ form.name ? form.name.toUpperCase() : '' }}</span>
          <span class="field field-birth-month">{{ form.birthMonth ? String(form.birthMonth).toUpperCase() : '' }}</span>
          <span class="field field-birth-day">{{ form.birthDay ? String(form.birthDay).toUpperCase() : '' }}</span>
          <span class="field field-birth-year">{{ form.birthYear ? String(form.birthYear).toUpperCase() : '' }}</span>

          <span class="check check-sex-male">{{ form.sex === 'male' ? 'X' : '' }}</span>
          <span class="check check-sex-female">{{ form.sex === 'female' ? 'X' : '' }}</span>

          <span class="field field-age">{{ form.age ? form.age.toString().toUpperCase() : '' }}</span>
          <span class="field field-address field-tight">{{ form.address ? form.address.toUpperCase() : '' }}</span>
          <span class="field field-citizenship field-tight">{{ form.citizenship ? form.citizenship.toUpperCase() : '' }}</span>
          <span class="field field-contact field-tight">{{ form.contactNumber ? String(form.contactNumber).toUpperCase() : '' }}</span>
          <span class="field field-email field-tight">{{ form.email ? form.email.toUpperCase() : '' }}</span>

          <span class="check check-first-yes">{{ form.isFirstTime === 'yes' ? 'X' : '' }}</span>
          <span class="check check-first-no">{{ form.isFirstTime === 'no' ? 'X' : '' }}</span>
          <span class="field field-times-taken">{{ form.timesTaken ? String(form.timesTaken).toUpperCase() : '' }}</span>

          <span class="check check-app-shs">{{ form.applicantType === 'senior_high_student' ? 'X' : '' }}</span>
          <span class="field field-shs-school field-tight">{{ form.applicantType === 'senior_high_student' ? (form.schoolName ? String(form.schoolName).toUpperCase() : '') : '' }}</span>
          <span class="field field-shs-grad">{{ form.applicantType === 'senior_high_student' ? (form.graduationDate ? String(form.graduationDate).toUpperCase() : '') : '' }}</span>
          <span class="field field-shs-address field-tight">{{ form.applicantType === 'senior_high_student' ? (form.schoolAddress ? String(form.schoolAddress).toUpperCase() : '') : '' }}</span>

          <span class="check check-app-shg">{{ form.applicantType === 'senior_high_graduate' ? 'X' : '' }}</span>
          <span class="field field-shg-school field-tight">{{ form.applicantType === 'senior_high_graduate' ? (form.schoolName ? String(form.schoolName).toUpperCase() : '') : '' }}</span>
          <span class="field field-shg-grad">{{ form.applicantType === 'senior_high_graduate' ? (form.graduationDate ? String(form.graduationDate).toUpperCase() : '') : '' }}</span>
          <span class="field field-shg-address field-tight">{{ form.applicantType === 'senior_high_graduate' ? (form.schoolAddress ? String(form.schoolAddress).toUpperCase() : '') : '' }}</span>

          <span class="check check-app-college">{{ form.applicantType === 'college_student' ? 'X' : '' }}</span>
          <span class="field field-college-school field-tight">{{ form.applicantType === 'college_student' ? (form.schoolName ? String(form.schoolName).toUpperCase() : '') : '' }}</span>
          <span class="field field-college-course field-tight">{{ form.applicantType === 'college_student' ? (form.course ? String(form.course).toUpperCase() : '') : '' }}</span>
          <span class="field field-college-address field-tight">{{ form.applicantType === 'college_student' ? (form.schoolAddress ? String(form.schoolAddress).toUpperCase() : '') : '' }}</span>

          <span class="field field-test-date field-table">{{ appointmentInfo.test_date ? formatAppointmentDate(appointmentInfo.test_date).toUpperCase() : ((appointmentInfo.date) ? formatAppointmentDate(appointmentInfo.date).toUpperCase() : 'TO BE ASSIGNED') }}</span>
          <span class="field field-test-center field-table">{{ appointmentInfo.test_center ? appointmentInfo.test_center.toUpperCase() : 'TO BE ASSIGNED' }}</span>
          <span class="field field-room field-table">{{ (appointmentInfo.room_number ? (String(appointmentInfo.room_number) + (appointmentInfo.room_code ? ' ' + String(appointmentInfo.room_code) : '')).toUpperCase() : 'TO BE ASSIGNED') }}</span>
          <span class="field field-time field-table">{{ appointmentInfo.time_slot ? formatTimeSlot(appointmentInfo.time_slot).toUpperCase() : 'TO BE ASSIGNED' }}</span>
          <span class="field field-center-code field-table">{{ appointmentInfo.test_center_code ? String(appointmentInfo.test_center_code).toUpperCase() : 'TO BE ASSIGNED' }}</span>
          <span class="field field-hs-code field-table">{{ form.highSchoolCode ? String(form.highSchoolCode).toUpperCase() : 'NOT PROVIDED' }}</span>

          <div class="photo photo-top"></div>

          <span class="field field-permit-name field-tight">{{ form.name ? form.name.toUpperCase() : '' }}</span>
          <span class="field field-permit-school field-tight">{{ form.schoolName ? form.schoolName.toUpperCase() : '' }}</span>

          <span class="field field-permit-test-date field-table">{{ appointmentInfo.test_date ? formatAppointmentDate(appointmentInfo.test_date).toUpperCase() : ((appointmentInfo.date) ? formatAppointmentDate(appointmentInfo.date).toUpperCase() : 'TO BE ASSIGNED') }}</span>
          <span class="field field-permit-test-center field-table">{{ appointmentInfo.test_center ? appointmentInfo.test_center.toUpperCase() : 'TO BE ASSIGNED' }}</span>
          <span class="field field-permit-room field-table">{{ (appointmentInfo.room_number ? (String(appointmentInfo.room_number) + (appointmentInfo.room_code ? ' ' + String(appointmentInfo.room_code) : '')).toUpperCase() : 'TO BE ASSIGNED') }}</span>
          <span class="field field-permit-time field-table">{{ appointmentInfo.time_slot ? formatTimeSlot(appointmentInfo.time_slot).toUpperCase() : 'TO BE ASSIGNED' }}</span>
          <span class="field field-permit-center-code field-table">{{ appointmentInfo.test_center_code ? String(appointmentInfo.test_center_code).toUpperCase() : 'TO BE ASSIGNED' }}</span>
          <span class="field field-permit-hs-code field-table">{{ form.highSchoolCode ? String(form.highSchoolCode).toUpperCase() : 'NOT PROVIDED' }}</span>

          <span class="check check-student-shs">{{ form.applicantType === 'senior_high_student' ? 'X' : '' }}</span>
          <span class="check check-student-shg">{{ form.applicantType === 'senior_high_graduate' ? 'X' : '' }}</span>
          <span class="check check-student-wmsu-main">{{ form.applicantType === 'college_student' && form.collegeType === 'wmsu_main' ? 'X' : '' }}</span>
          <span class="check check-student-wmsu-external">{{ form.applicantType === 'college_student' && form.collegeType === 'wmsu_external' ? 'X' : '' }}</span>
          <span class="check check-student-non-wmsu">{{ form.applicantType === 'college_student' && form.collegeType === 'non_wmsu' ? 'X' : '' }}</span>

          <div class="photo photo-bottom"></div>
        </div>
      </div>
    </div>
    
    <div v-if="!outputPdfOnly" class="flex justify-center mt-4 print:hidden" :class="{ 'flex-col space-y-2 px-4': popupMode && isMobileView }">
      <template v-if="!popupMode">
        <button @click="printForm" class="bg-wmsu text-white px-6 py-2 rounded-lg mr-2 hover:bg-red-700 transition">Print Form</button>
        <button @click="downloadPDF" class="bg-green-600 text-white px-6 py-2 rounded-lg mr-2 hover:bg-green-700 transition">Download PDF</button>
        <button @click="router.push('/schedule')" class="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition mr-2">
          <i class="fas fa-arrow-left mr-2"></i>Return to Schedule
        </button>
        <button @click="reloadData" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition mr-2">
          <i class="fas fa-sync-alt mr-2"></i>Reload Data
        </button>
        <button @click="enhancedRefreshTestDetails" class="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition mr-2">
          <i class="fas fa-redo-alt mr-2"></i>Refresh Test Details
        </button>
        <button @click="showDebugInfo" class="bg-gray-700 text-white px-6 py-2 rounded-lg hover:bg-gray-800 transition">
          <i class="fas fa-bug mr-2"></i>Debug Info
        </button>
      </template>
      
      <template v-else>
        <div :class="{ 'w-full flex justify-center': isMobileView }">
          <button @click="downloadPDF" class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition" :class="{ 'w-full max-w-xs': isMobileView }">
          <i class="fas fa-file-download mr-2"></i>Download PDF
        </button>
        </div>
        
        <button v-if="!hasTestDetails" @click="fetchTestDetails(appointmentInfo.id)" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition" :class="{ 'mt-2 ml-0': isMobileView, 'ml-2': !isMobileView }">
          <i class="fas fa-sync-alt mr-2"></i>Refresh Test Details
        </button>
      </template>
    </div>
    
    <div v-if="debugModalVisible && !popupMode && !outputPdfOnly" class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50 print:hidden">
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-3xl w-full max-h-[80vh] overflow-auto">
        <h3 class="text-lg font-bold mb-4">Test Details Debug Information</h3>
        
        <div class="mb-4">
          <h4 class="font-semibold">Appointment ID: {{ appointmentInfo.id || 'Not set' }}</h4>
          <p class="text-sm text-gray-600">Last updated: {{ new Date(appointmentInfo.forceUpdate).toLocaleString() }}</p>
        </div>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <h4 class="font-semibold mb-2">Test Session</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">{{ JSON.stringify({
              test_date: appointmentInfo.test_date,
              exam_type: appointmentInfo.exam_type
            }, null, 2) }}</pre>
          </div>
          
          <div>
            <h4 class="font-semibold mb-2">Test Center</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">{{ JSON.stringify({
              test_center: appointmentInfo.test_center,
              test_center_code: appointmentInfo.test_center_code
            }, null, 2) }}</pre>
          </div>
          
          <div>
            <h4 class="font-semibold mb-2">Test Room</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">{{ JSON.stringify({
              room_number: appointmentInfo.room_number,
              room_code: appointmentInfo.room_code
            }, null, 2) }}</pre>
          </div>
          
          <div>
            <h4 class="font-semibold mb-2">Time Slot</h4>
            <pre class="bg-gray-100 p-2 rounded text-xs">{{ JSON.stringify({
              time_slot: appointmentInfo.time_slot,
              timeSlot: appointmentInfo.timeSlot,
              formatted: formatTimeSlot(appointmentInfo.time_slot || appointmentInfo.timeSlot)
            }, null, 2) }}</pre>
          </div>
        </div>
        
        <div class="mb-4">
          <h4 class="font-semibold mb-2">Complete AppointmentInfo Object</h4>
          <pre class="bg-gray-100 p-2 rounded text-xs max-h-40 overflow-auto">{{ JSON.stringify(appointmentInfo, null, 2) }}</pre>
        </div>
        
        <div class="mb-4 flex flex-wrap gap-2">
          <button 
            @click="forceTimeSlotRefresh" 
            class="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
          >
            <i class="fas fa-sync-alt mr-2"></i>Force Refresh Time Slot
          </button>
          <button 
            @click="clearTimeSlotCache" 
            class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            <i class="fas fa-eraser mr-2"></i>Clear Time Slot Cache
          </button>
          <button 
            @click="tryAllTimeSlotEndpoints" 
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            <i class="fas fa-search mr-2"></i>Try All API Endpoints
          </button>
        </div>
        
        <div class="flex justify-end">
          <button @click="debugModalVisible = false" class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, nextTick, computed } from 'vue'
import html2pdf from 'html2pdf.js'
import ApplicationFormStore from '@/services/ApplicationFormStore'
import { useRouter, useRoute } from 'vue-router'
import axiosInstance from '../services/axios.interceptor'
import axios from 'axios'

// Props
const props = defineProps({
  popupMode: {
    type: Boolean,
    default: false
  },
  appointmentData: {
    type: Object,
    default: null
  },
  outputPdfOnly: { // New prop
    type: Boolean,
    default: false
  },
  startDownload: { // New prop
    type: Boolean,
    default: false
  }
})

// Emit
const emit = defineEmits(['close', 'pdf-generation-complete'])

const formContainer = ref(null)
const isMobileView = ref(false)
const debugModalVisible = ref(false)

const schoolYear = ref('2025-2026');
const appointmentInfo = reactive({
  id: '',
  test_date: '',
  test_center: '',
  test_center_code: '',
  room_number: '',
  room_code: '',
  time_slot: '',
  exam_type: '',
  date: '',
  forceUpdate: 0
});

const form = reactive({
  name: '',
  birthMonth: '',
  birthDay: '',
  birthYear: '',
  sex: '',
  age: '',
  address: '',
  citizenship: '',
  contactNumber: '',
  email: '',
  highSchoolCode: '',
  schoolName: '',
  schoolAddress: '',
  graduationDate: '',
  course: '',
  collegeType: '',
  isFirstTime: 'yes',
  timesTaken: '',
  applicantType: ''
});
const hasTestDetails = computed(() => !!(appointmentInfo.test_date && appointmentInfo.test_center && appointmentInfo.room_number));
const formData = computed(() => (props.popupMode || props.outputPdfOnly) ? props.appointmentData : ApplicationFormStore.state.formData)
const hasSubmittedData = computed(() => (props.popupMode || props.outputPdfOnly) ? true : ApplicationFormStore.state.hasSubmittedData)

const router = useRouter();
const route = useRoute();

const loadFormData = () => {
  if (!hasSubmittedData.value) {
    return;
  }
  
  try {
    const testFormData = formData.value;
    if (!testFormData) {
      console.warn("[ApplicationForm] loadFormData called but formData.value (props.appointmentData) is null/undefined");
      return;
    }

    if (props.outputPdfOnly) {
      console.log('[ApplicationForm outputPdfOnly] Received testFormData:', testFormData);
    }

    const serverPayload = testFormData.serverModel || testFormData.serverResponse || {};
    
    // Personal Information
    form.name = testFormData.fullName || '';
    form.birthMonth = testFormData.birthMonth || '';
    form.birthDay = testFormData.birthDay || '';
    form.birthYear = testFormData.birthYear || '';
    // Handle gender which can be a string (from AppointmentStatus) or an object (from Profile)
    if (typeof testFormData.gender === 'object' && testFormData.gender !== null) {
      form.sex = testFormData.gender.male ? 'male' : (testFormData.gender.female ? 'female' : '');
    } else if (typeof testFormData.gender === 'string') {
      form.sex = testFormData.gender.toLowerCase();
    } else {
      form.sex = '';
    }
    form.age = testFormData.age || '';
    form.address = testFormData.homeAddress || '';
    form.citizenship = testFormData.citizenship || '';
    form.contactNumber = testFormData.contactNumber || '';
    form.email = testFormData.email || '';
    
    // Appointment / Test Info
    if (testFormData.appointmentId || testFormData.id) {
      const appointmentId = testFormData.appointmentId || testFormData.id;
      appointmentInfo.id = appointmentId;
      appointmentInfo.date = testFormData.preferredDate || testFormData.preferred_date;
      
      // Map test details from props if available
      if (testFormData.test_date) appointmentInfo.test_date = testFormData.test_date;
      if (testFormData.test_center) appointmentInfo.test_center = testFormData.test_center;
      if (testFormData.test_center_code) appointmentInfo.test_center_code = testFormData.test_center_code;
      if (testFormData.room_number) appointmentInfo.room_number = testFormData.room_number;
      if (testFormData.room_code) appointmentInfo.room_code = testFormData.room_code;
      if (testFormData.exam_type) appointmentInfo.exam_type = testFormData.exam_type;
      
      // Fallback for test_date if it's missing but we have session info
      if (!appointmentInfo.test_date && testFormData.test_session_exam_date) {
        appointmentInfo.test_date = testFormData.test_session_exam_date;
      }

      if (testFormData.timeSlot || testFormData.time_slot) {
        const slot = testFormData.timeSlot || testFormData.time_slot;
        appointmentInfo.time_slot = slot;
        appointmentInfo.reporting_time = slot === 'morning' ? '7:30 AM' : '12:30 PM';
      }

      // If in interactive mode and details are missing, fetch them
      if (!props.outputPdfOnly) {
        setTimeout(() => {
          fetchTestDetails(appointmentId);
        }, 500);
      }
    }

    // Applicant Type and School Info Mapping
    const applicantTypeMapping = {
      'senior_high_graduating': 'senior_high_student',
      'senior_high_graduate': 'senior_high_graduate',
      'college': 'college_student',
      // Handle already-normalized values
      'senior_high_student': 'senior_high_student',
      'college_student': 'college_student'
    };
    const applicantTypeRaw = testFormData.applicantType || testFormData.applicant_type || serverPayload.applicant_type || '';
    form.applicantType = applicantTypeMapping[applicantTypeRaw] || applicantTypeRaw || '';
    
    form.schoolName = ''; // Reset before conditional assignment
    form.schoolAddress = '';
    form.graduationDate = '';
    form.course = '';
    form.collegeType = '';

    const isSeniorGraduating = applicantTypeRaw === 'senior_high_graduating' || form.applicantType === 'senior_high_student';
    const isSeniorGraduate = applicantTypeRaw === 'senior_high_graduate' || form.applicantType === 'senior_high_graduate';
    const isCollegeStudent = applicantTypeRaw === 'college' || form.applicantType === 'college_student';

    if (isSeniorGraduating) {
      form.schoolName = testFormData.seniorGraduating?.schoolName || testFormData.schoolName || serverPayload.school_name || '';
      form.schoolAddress = testFormData.seniorGraduating?.schoolAddress || testFormData.schoolAddress || testFormData.school_address || serverPayload.school_address || '';
      form.graduationDate = testFormData.seniorGraduating?.graduationDate || testFormData.graduationDate || testFormData.school_graduation_date || serverPayload.school_graduation_date || '';
    } else if (isSeniorGraduate) {
      form.schoolName = testFormData.seniorGraduate?.schoolName || testFormData.schoolName || serverPayload.school_name || '';
      form.schoolAddress = testFormData.seniorGraduate?.schoolAddress || testFormData.schoolAddress || testFormData.school_address || serverPayload.school_address || '';
      form.graduationDate = testFormData.seniorGraduate?.graduationDate || testFormData.graduationDate || testFormData.school_graduation_date || serverPayload.school_graduation_date || '';
    } else if (isCollegeStudent) {
      form.schoolName = testFormData.college?.schoolName || testFormData.schoolName || serverPayload.school_name || '';
      form.schoolAddress = testFormData.college?.schoolAddress || testFormData.schoolAddress || testFormData.school_address || serverPayload.school_address || '';
      form.course = testFormData.college?.course || testFormData.college_course || serverPayload.college_course || '';
      form.collegeType = testFormData.college?.collegeType || testFormData.college_type || serverPayload.college_type || '';
    } else {
      // Fallback for unknown applicantType, use top-level fields if available
      form.schoolName = testFormData.schoolName || serverPayload.school_name || '';
      form.schoolAddress = testFormData.schoolAddress || testFormData.school_address || serverPayload.school_address || '';
      form.graduationDate = testFormData.graduationDate || testFormData.school_graduation_date || serverPayload.school_graduation_date || '';
    }

    // Final global fallbacks if still empty
    if (!form.schoolName) form.schoolName = testFormData.schoolName || testFormData.school_name || serverPayload.school_name || '';
    if (!form.schoolAddress) form.schoolAddress = testFormData.schoolAddress || testFormData.school_address || serverPayload.school_address || '';
    if (!form.graduationDate) form.graduationDate = testFormData.graduationDate || testFormData.school_graduation_date || serverPayload.school_graduation_date || '';

    if (props.outputPdfOnly) {
      console.log('[ApplicationForm outputPdfOnly] Populated form object (School Info):',
        'form.applicantType:', form.applicantType,
        'form.schoolName:', form.schoolName,
        'form.schoolAddress:', form.schoolAddress,
        'form.graduationDate:', form.graduationDate,
        'form.course:', form.course,
        'form.collegeType:', form.collegeType
      );
      console.log('[ApplicationForm outputPdfOnly] MAPPED form.applicantType:', form.applicantType);
    }

    // WMSUCET experience mapping
    form.isFirstTime = 'yes'; // Default to yes
    form.timesTaken = '';
    if (testFormData.wmsucetExperience) {
      form.isFirstTime = testFormData.wmsucetExperience.firstTime ? 'yes' : 
                        (testFormData.wmsucetExperience.notFirstTime ? 'no' : 'yes');
      form.timesTaken = testFormData.wmsucetExperience.timesTaken || '';
    }

    if (props.outputPdfOnly) {
      console.log('[ApplicationForm outputPdfOnly] Populated form object (School Info):',
        'form.applicantType:', form.applicantType,
        'form.schoolName:', form.schoolName,
        'form.schoolAddress:', form.schoolAddress,
        'form.graduationDate:', form.graduationDate,
        'form.course:', form.course,
        'form.collegeType:', form.collegeType
      );
      console.log('[ApplicationForm outputPdfOnly] Populated form object (WMSUCET Experience):',
        'form.isFirstTime:', form.isFirstTime,
        'form.timesTaken:', form.timesTaken
      );
    }

    // High School Code mapping
    form.highSchoolCode = testFormData.highSchoolCode || '';

    if (props.outputPdfOnly) {
      console.log('[ApplicationForm outputPdfOnly] Populated form object (High School Code):',
        'form.highSchoolCode:', form.highSchoolCode
      );
    }
  } catch (error) {
    console.error('Error loading form data:', error);
  }
}

const downloadPDF = () => {
  if (!formContainer.value) {
    console.error("Form container ref is not available for PDF generation.");
    if (props.outputPdfOnly) {
      emit('pdf-generation-complete', { success: false });
    }
    return;
  }
  const options = {
    margin: 0,
    filename: `WMSU-CET-Application-${form.name || 'Form'}${appointmentInfo.id ? '-Appt' + appointmentInfo.id : ''}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true, logging: false, letterRendering: true, scrollY: 0, windowWidth: document.documentElement.offsetWidth },
    jsPDF: { unit: 'in', format: 'legal', orientation: 'portrait', compress: true, hotfixes: ["px_scaling"] },
    pagebreak: { avoid: ['tr', 'td'] },
    html2canvas: { 
      windowHeight: formContainer.value.offsetHeight + 200,
      windowWidth: formContainer.value.offsetWidth,
      onclone: (doc) => { /* ... */ }
    }
  };
  
  html2pdf().from(formContainer.value).set(options).save().then(() => {
    if (props.outputPdfOnly) {
      emit('pdf-generation-complete', { success: true });
    } else if (props.popupMode) {
    setTimeout(() => {
      emit('close');
    }, 1000);
  }
  }).catch(err => {
    console.error("Error generating PDF:", err);
    if (props.outputPdfOnly) {
      emit('pdf-generation-complete', { success: false, error: err });
    }
  });
}

const printForm = () => window.print();
const fetchTestDetails = async (id) => {
  if (!id) return;
  try {
    const response = await axiosInstance.get(`/api/appointments/${id}/test-details/`);
    const data = response.data;
    
    // Process test details - handle nested structure
    const testSession = data.test_session || (data.test_details && data.test_details.session);
    const testCenter = data.test_center || (data.test_details && data.test_details.center);
    const testRoom = data.test_room || (data.test_details && data.test_details.room);

    if (testSession) {
      appointmentInfo.test_date = testSession.exam_date || testSession.date;
      appointmentInfo.exam_type = testSession.exam_type || testSession.name;
    }
    
    if (testCenter) {
      appointmentInfo.test_center = testCenter.name || testCenter.center_name;
      appointmentInfo.test_center_code = testCenter.code || testCenter.id;
    }
    
    if (testRoom) {
      // Logic for room_number (similar to AppointmentStatus.vue)
      if (testRoom.name && testRoom.room_code && testRoom.name !== testRoom.room_code && !testRoom.name.includes(`Room ${testRoom.room_code}`)) {
        appointmentInfo.room_number = testRoom.name;
      } else if (testRoom.name && testRoom.name === testRoom.room_code) {
        appointmentInfo.room_number = `Room ${testRoom.room_code}`;
      } else if (testRoom.room_code) {
        appointmentInfo.room_number = `Room ${testRoom.room_code}`;
      } else {
        appointmentInfo.room_number = testRoom.name || "Room";
      }
      appointmentInfo.room_code = testRoom.room_code;
    }

    appointmentInfo.forceUpdate = Date.now();
  } catch (error) {
    console.warn('Error fetching test details for ApplicationForm:', error);
  }
};
const formatAppointmentDate = (dateString) => {
  if (!dateString) return ''; 
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      return ''; 
    }
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long',
      day: 'numeric'
    });
  } catch (e) {
    console.warn('Error formatting date:', dateString, e);
    return ''; 
  }
}
const formatTimeSlot = (slot) => {
  if (!slot) return ''; 
  if (slot === 'morning') {
    return 'Morning (8:00 AM - 12:00 PM)';
  } else if (slot === 'afternoon') {
    return 'Afternoon (1:00 PM - 5:00 PM)';
  }
  return slot.toString(); 
}
const getApplicantTypeTitle = (type) => {
  if (props.outputPdfOnly) {
    console.log('[ApplicationForm outputPdfOnly] getApplicantTypeTitle called with type:', type);
  }
  let title = '';
  switch(type) {
    case 'senior_high_student':
      title = 'SENIOR HIGH SCHOOL GRADUATING STUDENT';
      break;
    case 'senior_high_graduate':
      title = 'SENIOR HIGH SCHOOL GRADUATE who has not enrolled in college.';
      break;
    case 'college_student':
      title = 'COLLEGE STUDENT';
      break;
    default:
      title = ''; 
  }
  if (props.outputPdfOnly) {
    console.log('[ApplicationForm outputPdfOnly] getApplicantTypeTitle returning:', title);
  }
  return title;
};
const getSchoolLabel = () => { /* ... */ };
const getSecondaryLabel = () => { /* ... */ };
const reloadData = () => { /* ... */ };
const manualRefreshTestDetails = () => { /* ... */ };
const showDebugInfo = () => { debugModalVisible.value = true; };
const enhancedRefreshTestDetails = () => { /* ... */ };
const closePopup = () => emit('close');

const checkMobileView = () => {
  isMobileView.value = window.innerWidth < 768;
};

onMounted(async () => {
  checkMobileView();
  window.addEventListener('resize', checkMobileView);

  if ((props.popupMode || props.outputPdfOnly) && props.appointmentData) {
    loadFormData();
  } else if (!props.outputPdfOnly) { 
    const routeAppointmentId = route.params.appointmentId;
    if (routeAppointmentId) { /* ... */ }
    loadFormData(); 
  }

  if (props.outputPdfOnly && props.startDownload && props.appointmentData) {
     await nextTick(); 
     if (formContainer.value) {
        downloadPDF();
    } else {
        console.warn("outputPdfOnly: formContainer not ready on mount for initial startDownload");
     }
  }
});

watch(() => props.startDownload, async (newValue) => {
  if (newValue && props.outputPdfOnly) {
    if (!props.appointmentData) {
        console.warn("startDownload triggered in outputPdfOnly mode, but no appointmentData provided.");
        emit('pdf-generation-complete', { success: false, error: 'No data' });
    return;
  }
    if (!form.name) { 
      loadFormData();
    }
    await nextTick(); 
    if (formContainer.value) {
      downloadPDF();
    } else {
      console.error("Cannot start PDF download: formContainer ref is not available.");
      emit('pdf-generation-complete', { success: false, error: 'formContainer not found' });
    }
  }
});

watch(() => props.appointmentData, (newData) => {
    if (props.outputPdfOnly && newData) {
  loadFormData();
}
}, { deep: true });

watch(() => props.popupMode, (newVal) => {
  if (newVal) checkMobileView();
});

</script>

<style scoped>
.hidden-for-pdf-generation {
  position: absolute !important;
  left: -9999px !important;
  top: -9999px !important;
  z-index: -1 !important;
  opacity: 0 !important;
  pointer-events: none !important;
  visibility: hidden !important;
  width: 8.5in !important; 
  height: 14in !important; 
  overflow: hidden !important;
}

@media print {
  @page {
    size: 8.5in 14in;
    margin: 0;
  }
  body {
    margin: 0;
    padding: 0;
    width: 8.5in;
    height: 14in;
  }
  .form-container {
    width: 8.5in;
    height: 14in;
    margin: 0;
    padding: 0.2in;
    box-sizing: border-box;
    box-shadow: none;
    border: none;
    transform: scale(0.98); 
    transform-origin: top center;
  }
}

.form-container {
  background-color: white;
  border: 1px solid #d1d5db;
  max-width: 8.5in;
  width: 100%;
  padding: 0;
  min-height: 14in;
  height: 14in;
  margin: 0 auto;
  box-sizing: border-box;
  page-break-after: always;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  font-family: Arial, Helvetica, sans-serif;
  position: relative;
}

:deep([class*='popup-mode']) .form-container {
  margin: 0;
  border: none;
  box-shadow: none;
}

.text-wmsu { color: #bf0000; }
.bg-wmsu { background-color: #bf0000; }
.border-wmsu { border-color: #bf0000; }

.form-bg-wrap {
  position: relative;
  width: 100%;
  height: 100%;
}

.form-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.form-overlay {
  position: absolute;
  inset: 0;
  font-size: 12px;
  color: #000000;
}

.field {
  position: absolute;
  line-height: 1.4;
  white-space: nowrap;
  overflow: visible;
  letter-spacing: -0.1px;
  font-weight: bold;
}

.field-tight {
  font-size: 10px;
  letter-spacing: -0.2px;
  transform: scaleX(0.9);
  transform-origin: left center;
}

.field-table {
  font-size: 8.5px;
  letter-spacing: -0.3px;
  transform: scaleX(0.8);
  transform-origin: center center;
}

.check {
  position: absolute;
  font-size: 14px;
  font-weight: bold;
  text-align: center;
  width: 0.18in;
  height: 0.18in;
  line-height: 0.18in;
}

.photo {
  position: absolute;
  width: 2in;
  height: 2in;
  overflow: hidden;
}

.photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* -------------------------------------
   Top section positions (inches) 
   Corrected Values applied here!
------------------------------------- */

.field-name { 
  left: 1.05in; 
  top: 2.41in; 
  width: 4.25in; 
  word-spacing: 0.45in;
  letter-spacing: 0.5px;
}
.field-birth-month { left: 6.33in; top: 2.45in; width: 0.3in; text-align: center; }
.field-birth-day { left: 6.71in; top: 2.45in; width: 0.3in; text-align: center; }
.field-birth-year { left: 7.12in; top: 2.45in; width: 0.45in; text-align: center; }

.check-sex-male { left: 1.79in; top: 2.94in; }
.check-sex-female { left: 2.31in; top: 2.94in; }

.field-age { left: 3.27in; top: 2.85in; width: 0.5in; text-align: center; letter-spacing: 0.18in; padding-left: 0.1in; }
.field-address { left: 5.00in; top: 2.89in; width: 3.63in; }

.field-citizenship { left: 1.15in; top: 3.27in; width: 1.25in; }
.field-contact { left: 3.20in; top: 3.27in; width: 1.0in; }
.field-email { left: 5.67in; top: 3.27in; width: 1.88in; }

.check-first-yes { left: 1.55in; top: 3.85in; }
.check-first-no { left: 2.21in; top: 3.77in; }
.field-times-taken { left: 6.35in; top: 3.85in; width: 1.25in; text-align: center; }

.check-app-shs { left: 0.60in; top: 4.25in; }
.field-shs-school { left: 1.85in; top: 4.47in; width: 3.7in; }
.field-shs-grad { left: 6.95in; top: 4.44in; width: 1.3in; text-align: center; }
.field-shs-address { left: 2.45in; top: 4.73in; width: 5.8in; }

.check-app-shg { left: 0.62in; top: 4.98in; }
.field-shg-school { left: 2.35in; top: 5.21in; width: 3.9in; }
.field-shg-grad { left: 6.35in; top: 5.21in; width: 1.3in; text-align: center; }
.field-shg-address { left: 1.67in; top: 5.49in; width: 6.15in; }

.check-app-college { left: 0.35in; top: 6.25in; }
.field-college-school { left: 2.1in; top: 6.15in; width: 3.45in; }
.field-college-course { left: 6.35in; top: 6.15in; width: 1.3in; }
.field-college-address { left: 1.55in; top: 6.38in; width: 6.15in; }

.field-test-date { left: 0.95in; top: 7.42in; width: 1.25in; text-align: center; }
.field-test-center { left: 2.35in; top: 7.42in; width: 1.6in; text-align: center; }
.field-room { left: 4.1in; top: 7.42in; width: 1.1in; text-align: center; }
.field-time { left: 5.25in; top: 7.42in; width: 1.1in; text-align: center; }
.field-center-code { left: 6.45in; top: 7.42in; width: 0.75in; text-align: center; }
.field-hs-code { left: 7.25in; top: 7.42in; width: 0.85in; text-align: center; }

.photo-top { right: 0.25in; top: 0.55in; }

/* Bottom section positions (inches) */

.field-permit-name { 
  left: 1.05in; 
  top: 9.54in; 
  width: 4.7in; 
  word-spacing: 0.45in;
  letter-spacing: 0.5px;
}
.field-permit-school { left: 1.05in; top: 9.87in; width: 4.7in; }

.field-permit-test-date { left: 1.15in; top: 10.95in; width: 1.2in; text-align: center; }
.field-permit-test-center { left: 2.55in; top: 10.95in; width: 1.6in; text-align: center; }
.field-permit-room { left: 4.25in; top: 10.95in; width: 1.05in; text-align: center; }
.field-permit-time { left: 5.35in; top: 10.95in; width: 1.1in; text-align: center; }
.field-permit-center-code { left: 6.52in; top: 10.95in; width: 0.75in; text-align: center; }
.field-permit-hs-code { left: 7.32in; top: 10.95in; width: 0.85in; text-align: center; }

.check-student-shs { left: 3.00in; top: 11.85in; }
.check-student-shg { left: 3.00in; top: 12.05in; }
.check-student-wmsu-main { left: 3.00in; top: 12.25in; }
.check-student-wmsu-external { left: 3.00in; top: 12.45in; }
.check-student-non-wmsu { left: 3.00in; top: 12.65in; }

.photo-bottom { right: 0.45in; top: 11.65in; }

/* General utility classes */
.field-line { border-bottom: 1px solid #bf0000; margin-bottom: 0.08in; position: relative; }
.dashed-line { border-top: 1px dashed #bf0000; margin: 0.3in 0; }
.instructions { padding-left: 16px; margin: 0; }
.photo-caption { max-width: 2.2in; }
.signature-block { max-width: 2.2in; }
.applicant-section { margin-top: 6px; }
.dob-labels { margin-right: 2px; }
.note-block { position: absolute; left: 0.15in; top: 0.8in; width: 1.6in; }

.vertical-ticket {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  position: absolute;
  left: -12px;
  top: 0.4in;
  height: 80%;
  border-right: 2px solid #bf0000;
  border-top: 1px solid #bf0000;
  border-bottom: 1px solid #bf0000;
  padding: 2px;
  text-align: center;
  font-weight: bold;
  font-size: 8px;
  color: #bf0000;
  background: white;
  width: 33px;
}

.section-spacing { margin-bottom: 0.1in; }
.table-spacing { margin: 0.1in 0; }
.top-section { min-height: 54%; overflow: visible; }
.bottom-section { min-height: 46%; overflow: visible; }

input[type="radio"], input[type="checkbox"] { accent-color: #bf0000; }
input { font-family: Arial, sans-serif; }
input[type="text"] { border: none; padding: 0; margin: 0; }

.pdf-friendly-input { margin-bottom: 5px; }
.input-container { border-bottom: 1px solid #000; min-height: 24px; position: relative; }

.input-text {
  position: relative;
  top: 0;
  display: block;
  width: 100%;
  padding: 1px 0;
  font-size: 11px;
  color: #000000;
}

@media print {
  .input-container { padding-top: 1mm !important; }
  .input-text {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    color: #000000 !important;
    font-weight: normal !important;
    font-size: 30px !important;
  }
}

.pdf-text {
  font-size: 10px;
  line-height: 1.2;
  padding: 1px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media print {
  .pdf-text { font-size: 11px !important; line-height: 1.1 !important; }
}

.form-text {
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  padding-bottom: 2px;
}

@media print {
  .form-text {
    bottom: 2px !important;
    line-height: 1.1 !important;
    font-family: Arial, sans-serif !important;
  }
  .border-b { min-height: 6mm !important; }
}

.pdf-line-container {
  position: relative;
  min-height: 20px;
  margin-top: 2px;
  padding-top: 2px;
}

.pdf-field-text {
  display: block;
  font-size: 11px;
  line-height: 1;
  padding-top: 2px;
  padding-bottom: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: Arial, sans-serif;
}

@media (max-width: 767px) {
  .form-container {
    transform: scale(0.95);
    transform-origin: top center;
  }
  button {
    font-size: 14px;
    padding: 10px 16px !important;
  }
}
</style>