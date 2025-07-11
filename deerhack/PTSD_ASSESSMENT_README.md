# PTSD Assessment Feature

## Overview
This feature provides a comprehensive PTSD assessment tool integrated into the MindGuard app. It includes category selection, questionnaire functionality, and detailed result analysis.

## Features

### 1. Category Selection Screen
- **Location**: `lib/app/view/category_selection_screen.dart`
- **Description**: Allows users to select from 5 PTSD categories:
  - **Abuse**: Physical, emotional, or sexual abuse experiences
  - **Assault**: Physical or sexual assault experiences  
  - **War/Combat**: Military combat or war-related trauma
  - **Accident**: Motor vehicle or other traumatic accidents
  - **Other**: Other traumatic experiences

### 2. Assessment Questionnaire Screen
- **Location**: `lib/app/view/assessment_questionnaire_screen.dart`
- **Description**: Presents 12 targeted questions for each category
- **Features**:
  - Progress tracking
  - Smooth page transitions
  - Answer validation
  - Auto-advance after selection
  - Previous/Next navigation

### 3. Assessment Result Screen
- **Location**: `lib/app/view/assessment_result_screen.dart`
- **Description**: Shows detailed results with:
  - Animated progress circle
  - Risk level assessment (Low, Moderate, High, Severe)
  - Personalized recommendations
  - Assessment summary
  - Options to retake or return to home

## Data Models

### 1. Assessment Models
- **Location**: `lib/app/model/assessment_model.dart`
- **Classes**:
  - `PTSDCategory`: Represents trauma categories
  - `AssessmentQuestion`: Individual questions
  - `AssessmentResponse`: User responses
  - `AssessmentResult`: Complete assessment results

### 2. Assessment Data
- **Location**: `lib/app/data/assessment_data.dart`
- **Contains**:
  - Pre-defined categories and questions
  - Scoring logic
  - Risk level calculations
  - Personalized recommendations

## Navigation

### Main Integration
The assessment feature is integrated into the home screen with a prominent button that leads users through the assessment flow:

1. **Home Screen** → Assessment Button
2. **Category Selection** → Choose trauma type
3. **Questionnaire** → Answer 12 questions
4. **Results** → View analysis and recommendations

### Routing
- **Router**: `lib/app/router.dart`
- **Demo Access**: `lib/demo/assessment_demo_page.dart`

## UI/UX Design

### Visual Design
- **Dark Theme**: Modern dark interface with blue accents
- **Gradient Cards**: Beautiful gradient backgrounds for categories
- **Smooth Animations**: Fade and slide transitions
- **Progress Indicators**: Visual feedback for completion status

### User Experience
- **Intuitive Flow**: Clear progression through assessment
- **Validation**: Ensures all questions are answered
- **Auto-advance**: Smooth transition between questions
- **Results Visualization**: Clear, animated results display

## Technical Implementation

### Key Dependencies
- Flutter Material Design
- Custom animations and transitions
- State management with providers
- Navigation and routing

### File Structure
```
lib/
├── app/
│   ├── model/
│   │   └── assessment_model.dart
│   ├── data/
│   │   └── assessment_data.dart
│   ├── view/
│   │   ├── category_selection_screen.dart
│   │   ├── assessment_questionnaire_screen.dart
│   │   └── assessment_result_screen.dart
│   └── router.dart
├── demo/
│   └── assessment_demo_page.dart
└── main.dart (updated with router)
```

## Assessment Categories & Questions

### Abuse Category
- Trust and relationship issues
- Emotional numbness and detachment
- Self-blame and guilt
- Hypervigilance and safety concerns

### Assault Category
- Flashbacks and intrusive memories
- Panic attacks and anxiety
- Avoidance behaviors
- Safety and trust issues

### War/Combat Category
- Survivor guilt
- Combat-related memories
- Hypervigilance
- Emotional detachment

### Accident Category
- Reliving traumatic events
- Avoidance of triggers
- Safety anxiety
- Intrusive thoughts

### Other Category
- General trauma symptoms
- Emotional distress
- Behavioral changes
- Sleep disturbances

## Risk Assessment

### Scoring System
- **Score Range**: 0-48 points (12 questions × 4 max points)
- **Risk Levels**:
  - **Low**: 0-40% (0-19 points)
  - **Moderate**: 40-60% (20-29 points)
  - **High**: 60-80% (30-38 points)
  - **Severe**: 80-100% (39-48 points)

### Recommendations
Each risk level provides specific recommendations:
- **Severe**: Immediate professional help, crisis support
- **High**: Professional therapy, daily coping strategies
- **Moderate**: Counseling consideration, stress management
- **Low**: Continued self-care, monitoring

## Usage Instructions

1. **Access Assessment**: Tap the "Take PTSD Assessment" button on the home screen
2. **Select Category**: Choose the trauma type that best fits your experience
3. **Answer Questions**: Complete all 12 questions honestly
4. **Review Results**: View your risk level and recommendations
5. **Take Action**: Follow the provided recommendations for your wellbeing

## Important Notes

- **Not Diagnostic**: This assessment is not a diagnostic tool
- **Professional Help**: Always consult mental health professionals for proper evaluation
- **Privacy**: All responses are handled securely within the app
- **Retake Option**: Users can retake the assessment at any time

## Future Enhancements

- Save assessment history
- Progress tracking over time
- Integration with therapy resources
- Customizable question sets
- Multi-language support

This comprehensive assessment feature provides users with valuable insights into their mental health while maintaining a supportive and professional approach to trauma-related concerns.
