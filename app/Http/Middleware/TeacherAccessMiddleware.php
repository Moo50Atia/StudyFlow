<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use App\Models\TeacherPermission;
use Illuminate\Support\Facades\Auth;

class TeacherAccessMiddleware
{
    /**
     * Handle an incoming request.
     * Checks if teacher has permission to access the resource.
     */
    public function handle(Request $request, Closure $next): Response
    {
        $user = Auth::user();

        if (!$user) {
            return redirect()->route('login');
        }

        // Admin has full access
        if ($user->role === 'admin') {
            return $next($request);
        }

        // Students can only view (index, show)
        if ($user->role === 'student') {
            $method = $request->method();
            $routeName = $request->route()->getName();

            // Allow only GET requests for index and show
            if ($method === 'GET' && (str_contains($routeName, '.index') || str_contains($routeName, '.show'))) {
                return $next($request);
            }

            abort(403, 'Students can only view content.');
        }

        // Teacher access check
        if ($user->role === 'teacher') {
            $routeName = $request->route()->getName();
            $method = $request->method();

            // Get the resource from route
            $lecture = $request->route('lecture');
            $subject = $request->route('subject');
            $section = $request->route('section');
            $question = $request->route('question');
            $examQuestion = $request->route('exam_question');

            // Check permissions based on route
            if ($lecture) {
                $hasPermission = TeacherPermission::where('teacher_id', $user->id)
                    ->where('lecture_id', $lecture->id)
                    ->exists();

                if (!$hasPermission && !in_array($method, ['GET'])) {
                    abort(403, 'You do not have permission to modify this lecture.');
                }
            }

            if ($subject) {
                $hasPermission = TeacherPermission::where('teacher_id', $user->id)
                    ->where('subject_id', $subject->id)
                    ->exists();

                if (!$hasPermission && !in_array($method, ['GET'])) {
                    abort(403, 'You do not have permission to modify this subject.');
                }
            }

            // For sections, questions, exam_questions - check via lecture
            if ($section) {
                $hasPermission = TeacherPermission::where('teacher_id', $user->id)
                    ->where('lecture_id', $section->lecture_id)
                    ->exists();

                if (!$hasPermission && !in_array($method, ['GET'])) {
                    abort(403, 'You do not have permission to modify this section.');
                }
            }

            if ($question) {
                $hasPermission = TeacherPermission::where('teacher_id', $user->id)
                    ->where('lecture_id', $question->lecture_id)
                    ->exists();

                if (!$hasPermission && !in_array($method, ['GET'])) {
                    abort(403, 'You do not have permission to modify this question.');
                }
            }

            if ($examQuestion) {
                $hasPermission = TeacherPermission::where('teacher_id', $user->id)
                    ->where('lecture_id', $examQuestion->lecture_id)
                    ->exists();

                if (!$hasPermission && !in_array($method, ['GET'])) {
                    abort(403, 'You do not have permission to modify this exam question.');
                }
            }
        }

        return $next($request);
    }
}
