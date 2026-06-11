# Component Patterns

Load this file when building typed React components, extending native elements, or modeling variant props with discriminated unions.

## Props — extend native elements

Use `ComponentPropsWithoutRef` to inherit all native element props without the ref type conflict.

```typescript
type ButtonProps = {
  variant: 'primary' | 'secondary';
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ variant, children, ...props }: ButtonProps) {
  return <button className={variant} {...props}>{children}</button>;
}
```

## Children typing

```typescript
type Props = {
  children: React.ReactNode;               // Anything renderable (strings, numbers, arrays, null)
  icon: React.ReactElement;                // Single React element only
  render: (data: T) => React.ReactNode;   // Render prop
  label: string | React.ReactElement;     // String or element
};
```

Never use `JSX.Element` for children — it excludes strings, numbers, arrays, fragments, and `null`.

## Discriminated unions for variant props

Model variants as discriminants so TypeScript narrows the type in each branch:

```typescript
type ButtonProps =
  | { variant: 'link'; href: string; onClick?: never }
  | { variant: 'button'; onClick: () => void; href?: never };

function Button(props: ButtonProps) {
  if (props.variant === 'link') {
    return <a href={props.href}>Link</a>;
  }
  return <button onClick={props.onClick}>Button</button>;
}
```

## Exhaustive checks on discriminated unions

When a switch/if is missing a case arm TypeScript narrows to `never`. Use `satisfies never` to get a compile error instead of a silent fallthrough:

```typescript
function renderVariant(props: ButtonProps) {
  switch (props.variant) {
    case 'link': return <a href={props.href} />;
    case 'button': return <button onClick={props.onClick} />;
    default: return props satisfies never; // compile error if case added without handling
  }
}
```

## Polymorphic components (as prop)

```typescript
type PolymorphicProps<T extends React.ElementType> = {
  as?: T;
  children: React.ReactNode;
} & React.ComponentPropsWithoutRef<T>;

function Box<T extends React.ElementType = 'div'>({
  as,
  children,
  ...props
}: PolymorphicProps<T>) {
  const Component = as ?? 'div';
  return <Component {...props}>{children}</Component>;
}

// Usage:
<Box as="section" aria-label="main content">...</Box>
<Box as="button" onClick={handleClick}>...</Box>
```

## Compound components

```typescript
type CardContextValue = { collapsible: boolean };
const CardContext = createContext<CardContextValue | null>(null);

function Card({ collapsible = false, children }: { collapsible?: boolean; children: React.ReactNode }) {
  return (
    <CardContext.Provider value={{ collapsible }}>
      <div className="card">{children}</div>
    </CardContext.Provider>
  );
}

function CardHeader({ children }: { children: React.ReactNode }) {
  const ctx = useContext(CardContext);
  if (!ctx) throw new Error('CardHeader must be inside Card');
  return <div className="card-header">{children}</div>;
}

Card.Header = CardHeader;
```

## Generic components

See [generic-components.md](../examples/generic-components.md) for Table, Select, List, Modal patterns with full `keyof T` typing.
