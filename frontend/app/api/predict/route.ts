import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { redFighter, blueFighter } = body;

    console.log('Prediction request received:', { redFighter: redFighter?.name, blueFighter: blueFighter?.name });

    if (!redFighter || !blueFighter) {
      return NextResponse.json(
        { error: 'Both red and blue fighters must be provided' },
        { status: 400 }
      );
    }

    // Path to the Python prediction script
    const scriptPath = path.join(process.cwd(), '..', 'prediction', 'predict_ensemble.py');
    const pythonPath = 'C:/Users/Smokable/code/cs_330/cs_330/.venv/Scripts/python.exe';

    console.log('Script path:', scriptPath);
    console.log('Python path:', pythonPath);
    console.log('Current working directory:', process.cwd());

    // Create a promise to handle the Python script execution
    const prediction = await new Promise<any>((resolve, reject) => {
      // Run the ensemble prediction script
      const pythonProcess = spawn(pythonPath, [
        scriptPath,
        '--red-fighter', redFighter.name,
        '--blue-fighter', blueFighter.name,
        '--output-format', 'json'
      ], {
        cwd: path.join(process.cwd(), '..'), // Set working directory to project root
        stdio: ['pipe', 'pipe', 'pipe']
      });

      let outputData = '';
      let errorData = '';

      pythonProcess.stdout.on('data', (data) => {
        outputData += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        errorData += data.toString();
      });

      pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code: ${code}`);
        console.log('Python stdout:', outputData);
        console.log('Python stderr:', errorData);
        
        if (code !== 0) {
          console.error(`Python script failed with code ${code}`);
          console.error('Error output:', errorData);
          reject(new Error(`Prediction failed: ${errorData || 'Unknown error'}`));
          return;
        }

        try {
          // Try to parse JSON from the output
          const lines = outputData.trim().split('\n');
          const jsonLine = lines.find(line => line.startsWith('{'));
          
          if (!jsonLine) {
            console.log('Full output:', outputData);
            reject(new Error('No JSON output found from prediction script'));
            return;
          }

          const result = JSON.parse(jsonLine);
          resolve(result);
        } catch (parseError) {
          console.error('Failed to parse prediction output:', outputData);
          reject(new Error(`Failed to parse prediction output: ${parseError}`));
        }
      });

      pythonProcess.on('error', (error) => {
        reject(new Error(`Failed to start prediction process: ${error.message}`));
      });
    });

    return NextResponse.json({
      success: true,
      prediction,
      fighters: {
        red: redFighter,
        blue: blueFighter
      }
    });

  } catch (error) {
    console.error('Prediction API error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error', 
        details: error instanceof Error ? error.message : String(error)
      },
      { status: 500 }
    );
  }
}