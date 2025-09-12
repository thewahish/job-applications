#!/bin/bash
# Duplicate Detection & Resolution Script for Job Applications
# Run this before starting any new job assessment

echo "=== JOB FOLDER DUPLICATE DETECTION & RESOLUTION ==="
echo ""

# Stage priority hierarchy (higher number = higher priority)
declare -A stage_priority
stage_priority["4_Archive"]=5
stage_priority["3_Applied"]=4
stage_priority["2_Preparation_Stage"]=3
stage_priority["1_Analysis_Stage"]=2
stage_priority["5_Cancelled"]=1

# Function to get stage priority
get_stage_priority() {
    local stage="$1"
    echo "${stage_priority[$stage]:-0}"
}

# Function to get stage display name
get_stage_display() {
    local stage="$1"
    case "$stage" in
        "1_Analysis_Stage") echo "Analysis" ;;
        "2_Preparation_Stage") echo "Preparation" ;;
        "3_Applied") echo "Applied" ;;
        "4_Archive") echo "Archive" ;;
        "5_Cancelled") echo "Cancelled" ;;
        *) echo "$stage" ;;
    esac
}

# Get all job folders across all stages
declare -A folder_locations
declare -A folder_priorities
duplicates_found=false
resolution_actions=()

# Function to process individual job folders
process_job_folder() {
    local folder_name="$1"
    local stage_display="$2"
    local stage_priority="$3"
    
    # Use full folder name as key (case-insensitive)
    folder_key=$(echo "$folder_name" | tr '[:upper:]' '[:lower:]')
    
    # Check if we've seen this exact folder name before
    if [[ -n "${folder_locations[$folder_key]}" ]]; then
        existing_location="${folder_locations[$folder_key]}"
        existing_priority="${folder_priorities[$folder_key]}"
        current_priority="$stage_priority"
        
        echo "    ⚠️  DUPLICATE DETECTED: $folder_name"
        echo "       Existing: $existing_location (Priority: $existing_priority)"
        echo "       Current:  $stage_display/$folder_name (Priority: $current_priority)"
        
        if [ "$current_priority" -gt "$existing_priority" ]; then
            echo "       ✅ KEEPING: $stage_display/$folder_name (Higher Priority)"
            echo "       ❌ REMOVING: $existing_location (Lower Priority)"
            resolution_actions+=("REMOVE:$existing_location")
            folder_locations["$folder_key"]="$stage_display/$folder_name"
            folder_priorities["$folder_key"]="$current_priority"
        elif [ "$current_priority" -eq "$existing_priority" ]; then
            echo "       ❌ ERROR: Same priority conflict - Manual resolution required"
            duplicates_found=true
        else
            echo "       ❌ REMOVING: $stage_display/$folder_name (Lower Priority)"
            echo "       ✅ KEEPING: $existing_location (Higher Priority)"
            resolution_actions+=("REMOVE:$stage_display/$folder_name")
        fi
        echo ""
    else
        folder_locations["$folder_key"]="$stage_display/$folder_name"
        folder_priorities["$folder_key"]="$stage_priority"
        echo "    ✅ $folder_name"
    fi
}

echo "Scanning all job folders across stages..."
echo ""

# Scan each stage directory in priority order (highest first)
for stage_dir in "Jobs/4_Archive" "Jobs/3_Applied" "Jobs/2_Preparation_Stage" "Jobs/1_Analysis_Stage" "Jobs/5_Cancelled"; do
    if [ -d "$stage_dir" ]; then
        stage_name=$(basename "$stage_dir")
        stage_priority=$(get_stage_priority "$stage_name")
        stage_display=$(get_stage_display "$stage_name")
        echo "Checking $stage_display (Priority: $stage_priority):"
        
        # Handle nested structure for all stages
        for category_dir in "$stage_dir"/*; do
            if [ -d "$category_dir" ]; then
                category_name=$(basename "$category_dir")
                
                # Skip system files and non-category folders
                if [[ "$category_name" == "OLD" || "$category_name" == ".*" || "$category_name" == *".md" || "$category_name" == *".png" ]]; then
                    continue
                fi
                
                # Check if this is a category folder (IT_Technology, Audio_Sound, Creative_Media)
                if [[ "$category_name" == "IT_Technology" || "$category_name" == "Audio_Sound" || "$category_name" == "Creative_Media" ]]; then
                    echo "  📁 $category_name category:"
                    for folder in "$category_dir"/*; do
                        if [ -d "$folder" ]; then
                            folder_name=$(basename "$folder")
                            
                            # Skip system files
                            if [[ "$folder_name" == "OLD" || "$folder_name" == ".*" ]]; then
                                continue
                            fi
                            
                            # Process job folder
                            process_job_folder "$folder_name" "$stage_display" "$stage_priority"
                        fi
                    done
                else
                    # Handle direct folders (legacy structure)
                    folder_name="$category_name"
                    process_job_folder "$folder_name" "$stage_display" "$stage_priority"
                fi
            fi
        done
        echo ""
    fi
done

# Process resolution actions
if [ ${#resolution_actions[@]} -gt 0 ]; then
    echo "=== AUTOMATIC DUPLICATE RESOLUTION ==="
    echo ""
    
    for action in "${resolution_actions[@]}"; do
        action_type=$(echo "$action" | cut -d':' -f1)
        target_path=$(echo "$action" | cut -d':' -f2-)
        
        if [ "$action_type" = "REMOVE" ]; then
            # Convert display format back to actual path
            stage_display=$(echo "$target_path" | cut -d'/' -f1)
            folder_name=$(echo "$target_path" | cut -d'/' -f2)
            
            case "$stage_display" in
                "Analysis") 
                    # Check nested structure for Analysis stage
                    actual_path=""
                    for category in "IT_Technology" "Audio_Sound" "Creative_Media"; do
                        if [ -d "Jobs/1_Analysis_Stage/$category/$folder_name" ]; then
                            actual_path="Jobs/1_Analysis_Stage/$category/$folder_name"
                            break
                        fi
                    done
                    # Fallback to direct path for legacy structure
                    if [ -z "$actual_path" ]; then
                        actual_path="Jobs/1_Analysis_Stage/$folder_name"
                    fi
                    ;;
                "Preparation") 
                    # Check nested structure for Preparation stage
                    actual_path=""
                    for category in "IT_Technology" "Audio_Sound" "Creative_Media"; do
                        if [ -d "Jobs/2_Preparation_Stage/$category/$folder_name" ]; then
                            actual_path="Jobs/2_Preparation_Stage/$category/$folder_name"
                            break
                        fi
                    done
                    # Fallback to direct path for legacy structure
                    if [ -z "$actual_path" ]; then
                        actual_path="Jobs/2_Preparation_Stage/$folder_name"
                    fi
                    ;;
                "Applied") 
                    # Check nested structure for Applied stage
                    actual_path=""
                    for category in "IT_Technology" "Audio_Sound" "Creative_Media"; do
                        if [ -d "Jobs/3_Applied/$category/$folder_name" ]; then
                            actual_path="Jobs/3_Applied/$category/$folder_name"
                            break
                        fi
                    done
                    # Fallback to direct path for legacy structure
                    if [ -z "$actual_path" ]; then
                        actual_path="Jobs/3_Applied/$folder_name"
                    fi
                    ;;
                "Archive") 
                    # Check nested structure for Archive stage
                    actual_path=""
                    for category in "IT_Technology" "Audio_Sound" "Creative_Media"; do
                        if [ -d "Jobs/4_Archive/$category/$folder_name" ]; then
                            actual_path="Jobs/4_Archive/$category/$folder_name"
                            break
                        fi
                    done
                    # Fallback to direct path for legacy structure
                    if [ -z "$actual_path" ]; then
                        actual_path="Jobs/4_Archive/$folder_name"
                    fi
                    ;;
                "Cancelled") 
                    # Check nested structure for Cancelled stage
                    actual_path=""
                    for category in "IT_Technology" "Audio_Sound" "Creative_Media"; do
                        if [ -d "Jobs/5_Cancelled/$category/$folder_name" ]; then
                            actual_path="Jobs/5_Cancelled/$category/$folder_name"
                            break
                        fi
                    done
                    # Fallback to direct path for legacy structure
                    if [ -z "$actual_path" ]; then
                        actual_path="Jobs/5_Cancelled/$folder_name"
                    fi
                    ;;
            esac
            
            if [ -d "$actual_path" ]; then
                echo "🗑️  Removing lower priority duplicate: $actual_path"
                rm -rf "$actual_path"
                if [ $? -eq 0 ]; then
                    echo "   ✅ Successfully removed"
                else
                    echo "   ❌ Failed to remove - manual cleanup required"
                    duplicates_found=true
                fi
            else
                echo "   ⚠️  Path not found: $actual_path (already removed?)"
            fi
        fi
    done
    echo ""
fi

# Final status check
if [ "$duplicates_found" = true ]; then
    echo "❌ MANUAL INTERVENTION REQUIRED"
    echo "   Some duplicates could not be automatically resolved."
    echo "   Please review conflicts and resolve manually."
    echo ""
    exit 1
else
    echo "✅ NO DUPLICATES FOUND - Safe to proceed with new job assessments!"
    if [ ${#resolution_actions[@]} -gt 0 ]; then
        echo "   (Automatic cleanup completed successfully)"
    fi
    echo ""
    exit 0
fi