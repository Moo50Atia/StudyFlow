<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Models\Subject;
use App\Models\Lecture;
use App\Models\Section;
use App\Models\Question;
use App\Models\ExamQuestion;
use App\Models\TeacherPermission;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class DashboardController extends Controller
{
    /**
     * Show the appropriate dashboard based on user role.
     */
    public function index()
    {

        if (!Auth::check()) {
            return redirect()->route('login');
        }
        $user = Auth::user();

        return match ($user->role) {
            'admin' => $this->adminDashboard(),
            'teacher' => $this->teacherDashboard(),
            'student' => $this->studentDashboard(),
            default => redirect()->route('login'),
        };
    }

    /**
     * Admin Dashboard - Full access to everything.
     */
    private function adminDashboard()
    {
        $stats = [
            'users' => User::count(),
            'subjects' => Subject::count(),
            'lectures' => Lecture::count(),
            'sections' => Section::count(),
            'questions' => Question::count(),
            'exam_questions' => ExamQuestion::count(),
        ];

        $recentUsers = User::latest()->take(5)->get();
        $recentSubjects = Subject::latest()->take(5)->get();
        $recentLectures = Lecture::with('subject')->latest()->take(5)->get();

        return view('dashboards.admin', compact('stats', 'recentUsers', 'recentSubjects', 'recentLectures'));
    }

    /**
     * Teacher Dashboard - Access based on TeacherPermission.
     */
    private function teacherDashboard()
    {
        $user = Auth::user();

        // Get teacher's permissions
        $permissions = TeacherPermission::where('teacher_id', $user->id)
            ->with(['subject', 'lecture'])
            ->get();

        $allowedSubjectIds = $permissions->pluck('subject_id')->unique();
        $allowedLectureIds = $permissions->pluck('lecture_id')->unique();

        // Get allowed content
        $subjects = Subject::whereIn('id', $allowedSubjectIds)->get();
        $lectures = Lecture::whereIn('id', $allowedLectureIds)->with('subject')->get();
        $sections = Section::whereIn('lecture_id', $allowedLectureIds)->with('lecture')->get();
        $questions = Question::whereIn('lecture_id', $allowedLectureIds)->with('lecture')->get();
        $examQuestions = ExamQuestion::whereIn('lecture_id', $allowedLectureIds)->with('lecture')->get();

        // Get loved items
        $lovedLectures = $user->lovedLectures()->with('subject')->get();
        $lovedQuestions = $user->lovedQuestions()->with('lecture')->get();
        $lovedExamQuestions = $user->lovedExamQuestions()->with('lecture')->get();

        return view('dashboards.teacher', compact(
            'subjects',
            'lectures',
            'sections',
            'questions',
            'examQuestions',
            'lovedLectures',
            'lovedQuestions',
            'lovedExamQuestions',
            'permissions'
        ));
    }

    /**
     * Student Dashboard - View only with loved items.
     */
    private function studentDashboard()
    {
        $user = Auth::user();

        // Get all content for viewing
        $subjects = Subject::withCount('lectures')->get();
        $recentLectures = Lecture::with('subject')->latest()->take(10)->get();

        // Get loved items
        $lovedLectures = $user->lovedLectures()->with('subject')->get();
        $lovedQuestions = $user->lovedQuestions()->with('lecture')->get();
        $lovedExamQuestions = $user->lovedExamQuestions()->with('lecture')->get();

        return view('dashboards.student', compact(
            'subjects',
            'recentLectures',
            'lovedLectures',
            'lovedQuestions',
            'lovedExamQuestions'
        ));
    }
}
