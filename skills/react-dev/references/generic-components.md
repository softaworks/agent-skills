# Generic Components

Load this file when building generic, reusable React components: Table, List, Select, Modal, FormField.

## Core pattern — keyof T for column keys

Generic components infer types from props — no manual type annotations at call sites.

```typescript
type Column<T> = {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], item: T) => React.ReactNode;
};

type TableProps<T> = {
  data: T[];
  columns: Column<T>[];
  keyExtractor: (item: T) => string | number;
  onRowClick?: (item: T) => void;
};

function Table<T>({ data, columns, keyExtractor, onRowClick }: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>{columns.map(col => <th key={String(col.key)}>{col.header}</th>)}</tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={keyExtractor(item)} onClick={() => onRowClick?.(item)}>
            {columns.map(col => (
              <td key={String(col.key)}>
                {col.render
                  ? col.render(item[col.key], item)
                  : String(item[col.key] ?? '')}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Usage — T is inferred as User
type User = { id: number; name: string; email: string };

<Table
  data={users}
  columns={[
    { key: 'name', header: 'Name' },
    { key: 'email', header: 'Email', render: val => <a href={`mailto:${val}`}>{String(val)}</a> },
  ]}
  keyExtractor={u => u.id}
/>
```

## Constrained generics — require specific properties

```typescript
type HasId = { id: string | number };

function List<T extends HasId>({
  items,
  renderItem,
}: {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}) {
  return <ul>{items.map(item => <li key={item.id}>{renderItem(item)}</li>)}</ul>;
}
```

## Generic Select / Combobox

```typescript
type SelectProps<T> = {
  options: T[];
  value: T | null;
  onChange: (value: T) => void;
  getLabel: (option: T) => string;
  getValue: (option: T) => string | number;
  placeholder?: string;
};

function Select<T>({ options, value, onChange, getLabel, getValue, placeholder }: SelectProps<T>) {
  return (
    <select
      value={value ? String(getValue(value)) : ''}
      onChange={e => {
        const selected = options.find(o => String(getValue(o)) === e.target.value);
        if (selected) onChange(selected);
      }}
    >
      {placeholder && <option value="">{placeholder}</option>}
      {options.map(option => (
        <option key={getValue(option)} value={String(getValue(option))}>
          {getLabel(option)}
        </option>
      ))}
    </select>
  );
}
```

## Generic Modal

```typescript
type ModalProps<T> = {
  isOpen: boolean;
  onClose: () => void;
  data: T | null;
  title: string;
  children: (data: T) => React.ReactNode;
};

function Modal<T>({ isOpen, onClose, data, title, children }: ModalProps<T>) {
  if (!isOpen || !data) return null;
  return (
    <dialog open aria-modal aria-label={title}>
      <button onClick={onClose} aria-label="Close">×</button>
      <h2>{title}</h2>
      {children(data)}
    </dialog>
  );
}

// Usage
<Modal isOpen={!!selectedUser} onClose={() => setSelectedUser(null)} data={selectedUser} title="User Details">
  {user => <UserCard user={user} />}
</Modal>
```

## Generic FormField

```typescript
type FormFieldProps<T extends Record<string, unknown>> = {
  name: keyof T & string;
  label: string;
  value: T[keyof T];
  onChange: (name: keyof T & string, value: T[keyof T]) => void;
  type?: 'text' | 'email' | 'number';
};

function FormField<T extends Record<string, unknown>>({
  name,
  label,
  value,
  onChange,
  type = 'text',
}: FormFieldProps<T>) {
  return (
    <label>
      {label}
      <input
        name={name}
        type={type}
        value={String(value ?? '')}
        onChange={e => onChange(name, e.target.value as T[keyof T])}
      />
    </label>
  );
}
```

## Tips

- Use `keyof T` (not `string`) for property keys — ensures the key exists on the data type.
- `render?: (value: T[keyof T], item: T)` gives access to both the cell value and the full row.
- Constrain generics (`T extends HasId`) when downstream code needs a guaranteed property.
- Avoid `any` in generic component implementations — use `unknown` and narrow explicitly.
