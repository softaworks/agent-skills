---
description: Add a skill to the project with validation and README generation
argument-hint: <source-path>
---

# Add Skill

Copy a skill from a source path to the project, verify naming consistency, and generate README.md if missing.

## Usage

```
/add-skill <source-path>
```

**Arguments:**
- `<source-path>` - Path to the skill directory to add (required)

**Examples:**
```
/add-skill ~/.claude/skills/my-skill
/add-skill ~/workspace/other-project/skills/awesome-skill
/add-skill /home/leo/workspace/softaworks/projects/claude-plugins/plugins/planning/skills/spec-interview
```

## Workflow

### 1. Validate Source Path

Check that the source path exists and is a directory:

```bash
if [ -d "<source-path>" ]; then
  echo "Source path exists"
else
  echo "Error: Source path does not exist or is not a directory"
  exit 1
fi
```

If source path is invalid, stop and report the error to the user.

### 2. Extract Skill Name

Get the skill name from the source path (basename of the directory):

```bash
basename <source-path>
```

Example: `/path/to/my-skill` → `my-skill`

Store this as the skill name for the rest of the workflow.

### 3. Copy Skill to Project

Copy the entire skill directory to `skills/`:

```bash
cp -r <source-path> skills/
```

Report to user: "✅ Copied skill to skills/[skill-name]"

### 4. Verify Folder Name is Kebab-Case

Check that the folder name follows kebab-case convention:
- Only lowercase letters, numbers, and hyphens
- No underscores, spaces, or uppercase letters

**Regex pattern:** `^[a-z0-9]+(-[a-z0-9]+)*$`

Use Bash to check:

```bash
skill_name="[skill-name]"
if [[ $skill_name =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Folder name is valid kebab-case"
else
  echo "Warning: Folder name is not kebab-case"
fi
```

If invalid, warn the user but continue (we'll check SKILL.md next).

### 5. Verify SKILL.md Exists and Read Frontmatter

Check for SKILL.md in the copied skill directory:

```bash
ls skills/[skill-name]/SKILL.md
```

If SKILL.md doesn't exist:
- Error and stop: "❌ Error: No SKILL.md found in skills/[skill-name]"
- Suggest: "Please ensure the source directory contains a valid SKILL.md file"

If SKILL.md exists, read it with the Read tool to extract the frontmatter.

**Extract the `name:` field from frontmatter:**

The frontmatter is between the first two `---` markers:

```yaml
---
name: skill-name-here
description: ...
---
```

Parse the YAML and extract the value of the `name:` field.

### 6. Verify Naming Consistency

Compare:
1. **Folder name:** `[skill-name]` (from basename)
2. **SKILL.md name field:** `[name-from-frontmatter]`

**Check 1: Both are kebab-case**

Both should match the regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

If either is not kebab-case:
- Report: "⚠️ Naming issue detected:"
  - If folder is not kebab-case: "  - Folder name '[folder]' is not kebab-case"
  - If name field is not kebab-case: "  - SKILL.md name '[name]' is not kebab-case"

**Check 2: Folder name matches name field**

If `folder-name` != `name-from-frontmatter`:
- Report: "⚠️ Name mismatch detected:"
  - "Folder name: [folder-name]"
  - "SKILL.md name: [name-from-frontmatter]"
  - "These should match for consistency"

**Ask user for fix:**

If there's a mismatch or non-kebab-case naming, ask:

"Would you like me to fix the naming inconsistency? I can:
1. Rename the folder to match SKILL.md name field
2. Update SKILL.md name field to match folder name
3. Leave as-is"

Based on user choice:
- **Option 1:** Use `mv` to rename the folder
- **Option 2:** Use Edit tool to update SKILL.md frontmatter
- **Option 3:** Continue without changes

Report the action taken.

### 7. Check for README.md

Check if README.md exists in the skill directory:

```bash
ls skills/[skill-name]/README.md
```

**If README.md exists:**
- Report: "✅ README.md already exists"
- Skip to step 8

**If README.md does NOT exist:**
- Report: "📝 No README.md found. Creating comprehensive README..."
- Proceed to spawn sub-agent

### 8. Spawn Sub-Agent to Create README.md (if missing)

Use the Task tool to spawn a general-purpose sub-agent with this prompt:

```
For the skill at /home/leo/workspace/softaworks/projects/agent-skills/skills/[skill-name]:

1. Read the SKILL.md file completely
2. Analyze what the skill does, how it works, and when to use it
3. Create a comprehensive README.md that explains:
   - **Purpose**: What the skill does and why it exists
   - **When to Use**: Specific scenarios and trigger phrases
   - **How It Works**: Step-by-step explanation of the workflow
   - **Key Features**: Main capabilities and highlights
   - **Usage Examples**: Practical examples showing how to use it
   - **Prerequisites** (if any): Required tools, dependencies, or setup
   - **Output** (if applicable): What the skill produces
   - **Best Practices** (if applicable): Tips for getting the best results

The README should be user-friendly, comprehensive, and help users understand the skill's purpose and functionality in detail.

Write the README.md to: skills/[skill-name]/README.md
```

**Agent parameters:**
- `subagent_type: "general-purpose"`
- `description: "Create README for [skill-name]"`

Wait for the agent to complete, then report success.

### 9. Add Plugin Entry to marketplace.json

Add a new plugin entry to `.claude-plugin/marketplace.json` for the new skill.

**Read the marketplace.json file** to get current plugins array.

**Ask user for category** using AskUserQuestion:

"Which category does this skill belong to?"

Options:
- ai-tools (AI-powered tools)
- meta (Skills for building skills/commands/plugins)
- documentation (Writing, diagrams, docs)
- design-frontend (UI/UX, React, styling)
- development (Database, dependencies, refactoring)
- planning (Requirements, implementation planning)
- professional (Communication, feedback)
- testing (QA, test planning)
- git (Version control)
- utilities (General tools)

**Create the plugin entry:**

```json
{
  "name": "[skill-name]",
  "description": "[description from SKILL.md frontmatter]",
  "source": "./",
  "strict": false,
  "skills": ["./skills/[skill-name]"],
  "category": "[selected-category]",
  "keywords": ["[category]", "[relevant]", "[tags]"]
}
```

**Insert the plugin entry** into the plugins array in marketplace.json, keeping entries grouped by category.

Use the Edit tool to add the new entry before the agents section (after the last skill entry for the selected category, or at the end of skills if it's a new category).

Report: "✅ Added plugin entry to marketplace.json"

### 10. Update Available Skills Table in README.md

Update the "Available Skills" table in README.md to include the new skill.

**Read README.md** to find the Available Skills table.

**Find the rows for the skill's category** and add the new skill in the appropriate position.

For example, if adding a skill to "🤖 AI Tools" category:
```markdown
| 🤖 AI Tools | [new-skill](skills/new-skill/README.md) | Description here |
```

Use the Edit tool to add the new row in the correct category section.

Report: "✅ Updated Available Skills table in README.md"

### 11. Final Report

After all steps are complete, report to the user:

```
✅ Skill '[skill-name]' added successfully!

📋 Summary:
- Source: <source-path>
- Destination: skills/[skill-name]
- SKILL.md: ✅ Valid
- Naming: [✅ Consistent / ⚠️ Fixed / ⚠️ Inconsistent]
- README.md: [✅ Exists / 📝 Created]
- marketplace.json: ✅ Plugin entry added
- Available Skills table: ✅ Updated

Next steps:
1. Review the skill at skills/[skill-name]
2. Commit the changes
```

## Error Handling

**Source path doesn't exist:**
- Stop immediately
- Error: "❌ Source path '<source-path>' does not exist"

**Source path is not a directory:**
- Stop immediately
- Error: "❌ Source path '<source-path>' is not a directory"

**No SKILL.md in source:**
- Stop after copy
- Error: "❌ No SKILL.md found in skills/[skill-name]"
- Suggest checking the source directory

**SKILL.md has no frontmatter:**
- Warn user
- Warning: "⚠️ SKILL.md has no frontmatter with name field"
- Ask if user wants to continue anyway

**Naming mismatch detected:**
- Warn user with details
- Offer to fix (rename folder or update frontmatter)
- Don't proceed until user decides

**README.md creation fails:**
- Report the failure
- Suggest: "You may need to create README.md manually for this skill"
- Continue anyway (skill is still added)

## Tools to Use

- **Bash** - Validate paths, copy directories, check naming
- **Read** - Read SKILL.md frontmatter, marketplace.json, README.md
- **Edit** - Fix SKILL.md name field, update marketplace.json, update README.md
- **Task** - Spawn sub-agent to create README.md
- **AskUserQuestion** - Ask about fixing naming inconsistencies, ask for category

## Success Criteria

- Skill copied to skills/ directory
- Folder name and SKILL.md name field are consistent and kebab-case
- README.md exists (either copied or created by sub-agent)
- Plugin entry added to marketplace.json
- Available Skills table in README.md updated
- User informed of all actions taken
- Clear next steps provided
