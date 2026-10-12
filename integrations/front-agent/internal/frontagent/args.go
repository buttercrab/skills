package frontagent

import (
	"fmt"
	"strings"
)

func splitArgs(args []string, valueFlags map[string]bool) ([]string, []string, error) {
	var flagArgs []string
	var positional []string
	for i := 0; i < len(args); i++ {
		arg := args[i]
		if arg == "--" {
			positional = append(positional, args[i+1:]...)
			break
		}
		if arg == "--help" || arg == "-h" {
			flagArgs = append(flagArgs, arg)
			continue
		}
		if !strings.HasPrefix(arg, "-") || arg == "-" {
			positional = append(positional, arg)
			continue
		}
		name := strings.TrimLeft(arg, "-")
		if before, _, ok := strings.Cut(name, "="); ok {
			name = before
		}
		takesValue, ok := valueFlags[name]
		if !ok {
			return nil, nil, fmt.Errorf("unknown flag: %s", arg)
		}
		flagArgs = append(flagArgs, arg)
		if !takesValue {
			continue
		}
		if strings.Contains(arg, "=") {
			continue
		}
		if i+1 >= len(args) {
			return nil, nil, fmt.Errorf("flag needs an argument: %s", arg)
		}
		i++
		flagArgs = append(flagArgs, args[i])
	}
	return flagArgs, positional, nil
}

func flattenArgs(args []any) []string {
	out := make([]string, 0, len(args))
	for _, arg := range args {
		switch value := arg.(type) {
		case string:
			if value != "" {
				out = append(out, value)
			}
		case []string:
			for _, item := range value {
				if item != "" {
					out = append(out, item)
				}
			}
		}
	}
	return out
}

func rootArgs(root string) []string {
	if strings.TrimSpace(root) == "" {
		return nil
	}
	return []string{"--root", root}
}

func flagProvided(args []string, name string) bool {
	long := "--" + name
	short := "-" + name
	for _, arg := range args {
		if arg == "--" {
			return false
		}
		if arg == long || strings.HasPrefix(arg, long+"=") || arg == short || strings.HasPrefix(arg, short+"=") {
			return true
		}
	}
	return false
}
