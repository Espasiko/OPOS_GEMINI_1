# Setup Guide - OpositaIA

## 🚀 Quick Start

### 1. Prerequisites

- **Node.js**: v20.0.0 or higher (v24.11.1 LTS recommended)
  - Download: https://nodejs.org/
  - Check version: `node --version`

- **npm**: v10.0.0 or higher (comes with Node.js)
  - Check version: `npm --version`

### 2. Install Dependencies

```bash
npm install
```

This will install all required packages including:

- React 19.2.0
- Google Gemini AI SDK
- Vite (build tool)
- TypeScript

### 3. Configure API Key

#### Get your Google Gemini API Key:

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key

#### Add API Key to your project:

1. Copy the example environment file:

   ```bash
   copy .env.example .env
   ```

2. Open `.env` file and replace `your_api_key_here` with your actual API key:

   ```
   VITE_API_KEY=AIzaSyC...your_actual_key_here
   ```

3. Save the file

**⚠️ IMPORTANT**: Never commit your `.env` file to Git! It's already in `.gitignore`.

### 4. Run the Development Server

```bash
npm run dev
```

The application will be available at:

- **Local**: http://localhost:3000/
- **Network**: http://[your-ip]:3000/

### 5. Build for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

To preview the production build:

```bash
npm run preview
```

## 🔧 Troubleshooting

### Error: "VITE_API_KEY environment variable not set"

**Solution**: Make sure you have:

1. Created a `.env` file in the root directory
2. Added your API key: `VITE_API_KEY=your_key_here`
3. Restarted the dev server (`npm run dev`)

### Error: "Unsupported engine"

**Solution**: Update Node.js to v20+ or v24.11.1 LTS

- Download: https://nodejs.org/

### Port 3000 already in use

**Solution**:

- Stop other processes using port 3000
- Or change the port in `vite.config.ts`

### API Key not working

**Solution**:

1. Verify your API key is correct
2. Check if the API key has the necessary permissions
3. Ensure you're not exceeding API rate limits
4. Visit: https://aistudio.google.com/app/apikey to check your key status

## 📚 Project Structure

```
/
├── components/          # React UI components
├── services/
│   └── geminiService.ts # Gemini API integration
├── docs/               # Documentation
│   ├── AI_AGENTS.md    # AI agent definitions
│   ├── ARCHITECTURE.md # System architecture
│   └── DATA_MODEL.md   # Data structures
├── ai-specs/           # AI development standards
├── .env                # Your API key (DO NOT COMMIT)
├── .env.example        # Template for .env
├── package.json        # Dependencies
└── vite.config.ts      # Vite configuration
```

## 🎯 Next Steps

1. **Read the documentation**:
   - `AI_SPECS_QUICKSTART.md` - AI Specs workflow
   - `docs/AI_AGENTS.md` - AI agent configurations
   - `README.md` - Project overview

2. **Try the features**:
   - Chat with the AI tutor
   - Generate practical cases
   - Create mind maps
   - Take mock exams

3. **Develop new features**:
   ```
   Kiro, planifica una nueva feature: [your idea]
   ```

## 🆘 Need Help?

- Check `AI_SPECS_QUICKSTART.md` for development workflow
- Review `docs/AI_AGENTS.md` for AI integration patterns
- Ask Kiro: "Explain how to [do something] in OpositaIA"

## 📝 Environment Variables Reference

| Variable       | Required | Description                                                       |
| -------------- | -------- | ----------------------------------------------------------------- |
| `VITE_API_KEY` | ✅ Yes   | Google Gemini API key from https://aistudio.google.com/app/apikey |

## 🔐 Security Notes

- **Never commit** your `.env` file
- **Never share** your API key publicly
- **Rotate your key** if it's accidentally exposed
- Use **environment-specific** keys for development/production

## 📦 Dependencies

### Production Dependencies

- `react` ^19.2.0 - UI framework
- `react-dom` ^19.2.0 - React DOM renderer
- `@google/genai` ^1.29.0 - Google Gemini AI SDK
- `html-to-image` ^1.11.13 - Export mind maps as images

### Development Dependencies

- `typescript` ~5.8.2 - Type safety
- `vite` ^6.2.0 - Build tool
- `@vitejs/plugin-react` ^5.0.0 - React plugin for Vite
- `@types/node` ^22.14.0 - Node.js type definitions

## 🌐 Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

## 📄 License

See LICENSE file for details.
