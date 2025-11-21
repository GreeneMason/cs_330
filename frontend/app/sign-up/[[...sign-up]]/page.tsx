import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="flex min-h-screen items-center justify-center" style={{ backgroundColor: '#000000' }}>
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Join Fight Predictor
          </h1>
          <p className="text-gray-400">
            Get access to AI-powered fight predictions
          </p>
        </div>
        <SignUp 
          appearance={{
            elements: {
              rootBox: "mx-auto",
              card: "bg-slate-900 border border-orange-400 shadow-xl",
              headerTitle: "text-white",
              headerSubtitle: "text-gray-400",
              socialButtonsBlockButton: "bg-slate-800 border border-slate-700 text-white hover:bg-slate-700",
              formFieldInput: "bg-slate-800 border border-slate-700 text-white",
              formButtonPrimary: "bg-orange-500 hover:bg-orange-600",
              footerActionLink: "text-orange-400 hover:text-orange-300"
            }
          }}
        />
      </div>
    </div>
  );
}