# Contributing to BIMFlow Suite

Thank you for your interest in contributing to BIMFlow Suite! We welcome contributions from developers, architects, engineers, and BIM professionals. This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Commit Messages](#commit-messages)
6. [Pull Request Process](#pull-request-process)
7. [Reporting Issues](#reporting-issues)
8. [Feature Requests](#feature-requests)
9. [Testing](#testing)
10. [Documentation](#documentation)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

**Be respectful** — Treat all community members with respect and professionalism.

**Be inclusive** — Welcome people of all backgrounds and experience levels.

**Be collaborative** — Work together constructively and share knowledge openly.

**Be constructive** — Provide helpful feedback and avoid harsh criticism.

## Getting Started

### Prerequisites

- Python 3.10+ (3.11+ recommended)
- Node.js 18+ with npm
- PostgreSQL 15+
- Redis 6+
- Git

### Fork & Clone

1. **Fork the repository** on GitHub
   ```bash
   Click "Fork" button on https://github.com/bimflow/bimflowsuite
   ```

2. **Clone your fork locally**
   ```bash
   git clone https://github.com/YOUR_USERNAME/bimflowsuite.git
   cd bimflowsuite
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/bimflow/bimflowsuite.git
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   # or for bug fixes:
   git checkout -b bugfix/issue-description
   ```

### Setup Development Environment

Follow the [Installation & Setup](README.md#installation--setup) section in the main README to set up your local development environment.

```bash
# Backend setup
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements/local.txt

# Frontend setup
cd ../bimflowsuite-ui
npm install
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/descriptive-feature-name
```

Branch naming conventions:
- `feature/` — New features
- `bugfix/` — Bug fixes
- `docs/` — Documentation updates
- `refactor/` — Code refactoring (no functional changes)
- `chore/` — Maintenance tasks (dependencies, CI/CD, etc.)
- `test/` — Test additions or fixes

### 2. Make Changes

**Backend Changes**

```bash
cd bimflowsuite

# Make your changes to Python files
# Example: Add new generator or compliance rule

# Run tests locally
DJANGO_SETTINGS_MODULE=config.settings.local pytest apps/ -v

# Check code style
flake8 apps/
black --check apps/
```

**Frontend Changes**

```bash
cd bimflowsuite-ui

# Make your changes to React/TypeScript files
# Example: Add new page or component

# Run tests
npm run test:run

# Check code style
npm run lint

# Build to verify no errors
npm run build
```

### 3. Commit Your Changes

See [Commit Messages](#commit-messages) section below for guidelines.

```bash
git add .
git commit -m "feat(generator): add parametric tunnel generation"
```

### 4. Keep Your Branch Updated

```bash
# Fetch latest changes from upstream
git fetch upstream

# Rebase your branch on upstream/main (or master)
git rebase upstream/main
```

### 5. Push to Your Fork

```bash
git push origin feature/my-feature
```

### 6. Create a Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill in the PR template with:
   - Clear title describing the change
   - Description of what changed and why
   - Related issues (use `Fixes #123` to auto-close)
   - Screenshots/GIFs if UI changes
   - Testing instructions

## Coding Standards

### Python (Backend)

**Follow PEP 8** with these tools:

```bash
# Code formatting
pip install black
black apps/ config/

# Linting
pip install flake8
flake8 apps/ config/

# Type checking
pip install mypy
mypy apps/
```

**Code Style Conventions**

```python
# ✅ Good: Clear naming, docstrings
def calculate_wall_clash_detection(wall_a: IfcWall, wall_b: IfcWall) -> ClashResult:
    """
    Detect geometric clashes between two wall elements.
    
    Args:
        wall_a: First wall entity
        wall_b: Second wall entity
        
    Returns:
        ClashResult object with clash details
    """
    # Implementation
    pass

# ❌ Bad: Unclear naming, no documentation
def calc_clash(w1, w2):
    pass
```

**Structure**

- Keep functions focused (single responsibility)
- Maximum function length: ~50 lines
- Maximum class length: ~200 lines
- Avoid deep nesting (max 3 levels)

### TypeScript/React (Frontend)

**Follow ESLint Configuration**

```bash
# Check style
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

**Component Structure**

```tsx
//Good: Clear exports, JSDoc, proper typing
interface ProjectCardProps {
  project: Project;
  onEdit: (id: number) => void;
}

/**
 * Displays a project summary card with quick actions.
 * @param {ProjectCardProps} props - Component props
 * @returns {JSX.Element}
 */
export const ProjectCard: React.FC<ProjectCardProps> = ({ project, onEdit }) => {
  return (
    <div className="card">
      {/* Component implementation */}
    </div>
  );
};

// Bad: Missing types, unclear purpose
export const Card = (props) => {
  return <div>{props.p}</div>;
};
```

**Naming Conventions**

- Components: `PascalCase` (e.g., `ProjectCard.tsx`)
- Hooks: `camelCase` starting with `use` (e.g., `useProjectData.ts`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `API_TIMEOUT`)
- Variables: `camelCase` (e.g., `projectName`)

### Comments & Documentation

**Python**

```python
# Use docstrings for modules, classes, and functions
"""
Module for parametric IFC generation from project specifications.
"""

class ProjectGenerator:
    """
    Generates IFC files from project specifications.
    
    Supports multiple asset types: building, road, bridge, tunnel.
    """
    
    def generate(self, spec: Dict) -> str:
        """Generate IFC string from specification."""
        pass
```

**TypeScript/React**

```typescript
// Use JSDoc comments
/**
 * Fetches project details from the API.
 * @param {number} projectId - The project ID
 * @returns {Promise<Project>} Project data
 * @throws {Error} If project not found
 */
async function fetchProject(projectId: number): Promise<Project> {
  return await api.get(`/projects/${projectId}`);
}
```

## Commit Messages

### Format

```
type(scope): subject line (50 chars max)

Detailed explanation of changes (72 chars per line)
- Bullet point 1
- Bullet point 2

Fixes #issue-number
Relates to #other-issue
```

### Types

- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation changes
- `style` — Code style (formatting, semicolons, etc.)
- `refactor` — Code refactoring (no functional change)
- `perf` — Performance improvements
- `test` — Test additions/modifications
- `chore` — Build, dependencies, CI/CD

### Scope

- `generator` — Parametric generator app
- `compliance` — Compliance engine app
- `analytics` — Analytics app
- `auth` — Authentication/users app
- `api` — REST API
- `ui` — Frontend/React components
- `config` — Configuration files
- `docs` — Documentation

### Examples

```
✅ Good examples:

feat(generator): add parametric tunnel generation
- Implement IfcBeamStandardCase for tunnel supports
- Add TunnelGenerator class with specifications
- Support cross-section variations

fix(compliance): handle missing ifc elements in rule evaluation
- Wrap rule conditions with try/except
- Log partial results when parsing fails
- Update ComplianceCheck status to "partial"

docs(readme): add PostgreSQL setup instructions

refactor(api): extract permission checks to middleware

perf(analytics): add database indexes for project queries

test(compliance): add clash detection tests for overlapping walls
```

## Pull Request Process

### Before Submitting

1. ✅ **Verify code changes work locally**
   ```bash
   # Backend
   DJANGO_SETTINGS_MODULE=config.settings.local pytest apps/ -v
   
   # Frontend
   npm run test:run && npm run build
   ```

2. ✅ **Check code style**
   ```bash
   # Backend
   flake8 apps/ && black --check apps/
   
   # Frontend
   npm run lint
   ```

3. ✅ **Update documentation** if needed
   - Update README.md for API changes
   - Add inline code comments for complex logic
   - Update ARCHITECTURE_DIAGRAMS.md for structural changes

4. ✅ **Rebase on latest upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### PR Checklist

- [ ] Branch is based on latest `main`
- [ ] Commits follow [commit message guidelines](#commit-messages)
- [ ] Code passes local tests (`pytest` and `npm run test:run`)
- [ ] Code follows style guidelines (`flake8`, `black`, `eslint`)
- [ ] Documentation is updated
- [ ] No breaking changes (or documented in PR)
- [ ] Changes are focused (not mixing multiple unrelated fixes)

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Fixes #123
Relates to #456

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How to test these changes:
1. Step 1
2. Step 2

## Screenshots (if UI changes)
[Add screenshots here]

## Checklist
- [ ] Tests pass locally
- [ ] Code style checks pass
- [ ] Documentation updated
- [ ] No breaking changes
```

## Reporting Issues

### Before Creating an Issue

1. Check existing issues (open and closed) — your issue may already be reported
2. Try reproducing with latest code
3. Check the [Troubleshooting Guide](README.md#troubleshooting-guide) in README

### Issue Title

Be specific and descriptive:

```
✅ Good: IFC generation fails for buildings with > 50 floors
❌ Bad: Generator broken
```

### Issue Description

Include:

1. **Description** — What's the problem?
2. **Steps to Reproduce**
   ```
   1. Create project with 60 floors
   2. Click "Generate IFC"
   3. Wait for completion
   ```
3. **Expected Behavior** — What should happen?
4. **Actual Behavior** — What actually happens?
5. **Environment**
   ```
   - OS: macOS 13.5
   - Python: 3.11.0
   - Django: 5.2.0
   ```
6. **Error Messages/Logs**
   ```
   Traceback (most recent call last):
     File "generators/building.py", line 42, in generate
   ValueError: Floor height must be > 0
   ```

### Issue Template

```markdown
## Description
[Your description here]

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: 
- Python Version: 
- Django Version: 
- Node.js Version: 

## Error Logs
[Paste error messages or logs]

## Screenshots
[If applicable]
```

## Feature Requests

Describe:

1. **Use Case** — Why do you need this?
2. **Proposed Solution** — How should it work?
3. **Alternative Solutions** — Any other approaches?
4. **Additional Context** — Anything else relevant?

```markdown
## Feature Request: Add IFC export to DWG format

### Use Case
Architects need to export compliance-checked IFC files to DWG for CAD integration.

### Proposed Solution
Add an export endpoint: POST /api/v1/generate/ifcs/{id}/export-dwg/

### Alternative Solutions
- Allow third-party DWG converters via API hook

### Additional Context
Most CAD tools still rely on DWG for interchange.
```

## Testing

### Backend Tests

```bash
cd bimflowsuite

# Run all tests
DJANGO_SETTINGS_MODULE=config.settings.local pytest apps/ -v

# Run specific app tests
DJANGO_SETTINGS_MODULE=config.settings.local pytest apps/compliance_engine/ -v

# Run specific test file
DJANGO_SETTINGS_MODULE=config.settings.local pytest apps/compliance_engine/tests/test_rule_engine.py -v

# Run with coverage
DJANGO_SETTINGS_MODULE=config.settings.local pytest apps/ --cov=apps --cov-report=html
```

### Frontend Tests

```bash
cd bimflowsuite-ui

# Run all tests
npm run test:run

# Run in watch mode (useful during development)
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific test file
npm run test src/components/ProjectCard.test.tsx
```

### Test Guidelines

1. **Write tests for new features**
   ```python
   # Backend example
   def test_parametric_tunnel_generation():
       spec = {
           "tunnel_length": 500,
           "tunnel_width": 10,
           "support_spacing": 5
       }
       ifc_string = generate_tunnel(spec)
       assert "IfcBeamStandardCase" in ifc_string
   ```

2. **Test edge cases**
   ```python
   # What happens with extreme values?
   test_with_zero_height()
   test_with_very_large_floor_count()
   test_with_invalid_materials()
   ```

3. **Test error handling**
   ```python
   # Does it fail gracefully?
   def test_generation_fails_with_invalid_spec():
       with pytest.raises(ValueError):
           generate_building({"floor_count": -1})
   ```

## Documentation

### Code Comments

Add comments for:
- Why, not what (code says what it does)
- Complex algorithms
- Non-obvious workarounds
- Performance-critical sections

```python
# ✅ Good: Explains why
# Use bounding box approximation instead of exact geometry
# to avoid expensive OpenCASCADE calculations for large models
bbox = calculate_aabb(element)

# ❌ Bad: Just restates code
# Create bounding box
bbox = calculate_aabb(element)
```

### README Updates

Update README.md if you:
- Add new API endpoints
- Change environment variables
- Add new features requiring setup
- Update dependencies

### Architecture Documentation

Update ARCHITECTURE_DIAGRAMS.md if you:
- Add new apps or major components
- Change data flow
- Modify database schema
- Update API routes

## Questions?

- **Documentation**: Check [README.md](README.md) and [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md)
- **Discussions**: Start a GitHub Discussion
- **Issues**: Create an issue with questions tag
- **Email**: support@bimflow.dev

## Recognition

Contributors who make significant improvements to the codebase will be recognized in:
- Release notes
- Contributors list in README
- Project documentation

---

## Additional Resources

- [README.md](README.md) — Project overview and setup
- [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) — System architecture
- [Django Contributing Guide](https://docs.djangoproject.com/en/5.2/internals/contributing/)
- [React Contributing Guide](https://react.dev/community/how-to-contribute)

Thank you for contributing to BIMFlow Suite! 🚀
